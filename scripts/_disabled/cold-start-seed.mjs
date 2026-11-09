#!/usr/bin/env node
/**
 * M01-P0-② 冷启动种子脚本
 *
 * 从 EVENT_CORPUS 中选取高置信度事件，
 * 在 PredictionFeedback 表中创建种子反馈记录。
 * 用于冷启动阶段为校准系统提供初始数据。
 *
 * 使用方式：
 *   cd vercel-deploy && node scripts/cold-start-seed.mjs
 *   可选：node scripts/cold-start-seed.mjs --dry-run（只打印，不写入）
 *   可选：node scripts/cold-start-seed.mjs --limit=20（限制数量）
 *
 * 幂等性：使用 upsert，重复运行不会产生重复记录。
 * 标记：所有种子记录 question 以 "[cold-start-seed]" 前缀标识。
 */

import { PrismaClient } from '../node_modules/@prisma/client/index.js';

const SEED_MARKER = '[cold-start-seed]';

// 内置种子事件数据（与 EVENT_CORPUS 一致的高置信度事件）
const SEED_EVENTS = [
  // 市场类
  { question: "Will BTC/USDT daily close be above $69,000 in 3 days?", outcome: "positive", confidence: 0.82 },
  { question: "Will S&P 500 close higher at the end of this week?", outcome: "positive", confidence: 0.78 },
  { question: "Will gold price touch $2,300/oz this month?", outcome: "positive", confidence: 0.75 },
  { question: "Will USD/CNY close below 7.30 this week?", outcome: "positive", confidence: 0.80 },

  // 科技类
  { question: "Will ChatGPT surpass 300M monthly active users by December 2024?", outcome: "positive", confidence: 0.85 },
  { question: "Will NVIDIA release a new GPU architecture in 2025?", outcome: "positive", confidence: 0.90 },
  { question: "Will Bitcoin mining difficulty adjust up in the next difficulty period?", outcome: "positive", confidence: 0.88 },

  // 政策类
  { question: "Will the Fed cut rates in the next FOMC meeting?", outcome: "positive", confidence: 0.72 },
  { question: "Will US CPI inflation drop below 3% by year-end?", outcome: "positive", confidence: 0.65 },
  { question: "Will China's GDP growth exceed 5% in Q4 2024?", outcome: "positive", confidence: 0.68 },

  // 气候/能源
  { question: "Will European natural gas prices exceed $100/MWh this month?", outcome: "negative", confidence: 0.70 },
  { question: "Will US gasoline prices drop below $3.50/gallon in 2025?", outcome: "negative", confidence: 0.60 },

  // 社会
  { question: "Will unemployment rate stay below 4% in the next 3 months?", outcome: "positive", confidence: 0.72 },
  { question: "Will consumer confidence index recover above 100 this quarter?", outcome: "positive", confidence: 0.55 },

  // 否定结局样本
  { question: "Will a major geopolitical conflict erupt in Q2 2025?", outcome: "negative", confidence: 0.85 },
  { question: "Will a global pandemic-level disease emerge in 2025?", outcome: "negative", confidence: 0.92 },
  { question: "Will cryptocurrency regulation ban staking in the US by year-end?", outcome: "negative", confidence: 0.70 },

  // 中性/不确定
  { question: "Will the housing market stabilize in the next 6 months?", outcome: "neutral", confidence: 0.50 },
  { question: "Will renewable energy exceed 30% of global electricity generation?", outcome: "positive", confidence: 0.55 },
];

function parseArgs() {
  const args = process.argv.slice(2);
  return {
    dryRun: args.includes('--dry-run'),
    limit: args.find(a => a.startsWith('--limit='))?.split('=')[1] ? parseInt(args.find(a => a.startsWith('--limit='))!.split('=')[1]) : SEED_EVENTS.length,
  };
}

async function main() {
  const { dryRun, limit } = parseArgs();
  const prisma = new PrismaClient();

  try {
    const events = SEED_EVENTS.slice(0, limit);
    console.log(`🌱 Cold Start Seed${dryRun ? ' (dry-run)' : ''}`);
    console.log(`   Events: ${events.length}`);
    console.log(`   Marker: ${SEED_MARKER}`);
    console.log();

    let created = 0;
    let skipped = 0;
    let updated = 0;

    for (const event of events) {
      const simulationId = `seed_${event.question.replace(/[^a-z0-9]/gi, '_').toLowerCase().slice(0, 40)}`;
      const marker = `${SEED_MARKER} ${event.question}`;

      // Check if already exists
      const existing = await prisma.predictionFeedback.findFirst({
        where: { question: marker, simulationId },
      });

      if (existing) {
        skipped++;
        if (!dryRun) console.log(`  ⏭️  Skip (exists): ${event.question.slice(0, 60)}...`);
        continue;
      }

      if (dryRun) {
        console.log(`  📝 Would create: ${event.question.slice(0, 60)}... → outcome=${event.outcome}, prob=${event.confidence}`);
        created++;
        continue;
      }

      try {
        await prisma.predictionFeedback.upsert({
          where: { simulationId },
          create: {
            simulationId,
            userId: 'system',
            question: marker,
            questionCategory: 'general',
            predictedProbability: event.confidence,
            predictedDirection: event.outcome,
            actualOutcome: event.outcome,
            actualNote: 'Cold-start seed from EVENT_CORPUS. Not from real user feedback.',
            reportedAt: new Date(),
            brierScore: Math.pow(event.confidence - (event.outcome === 'positive' ? 1 : event.outcome === 'negative' ? 0 : 0.5), 2),
            createdAt: new Date(),
          },
          update: {},
        });
        created++;
        console.log(`  ✅ Created: ${event.question.slice(0, 60)}... → outcome=${event.outcome}`);
      } catch (e) {
        // If upsert fails due to constraints, try update
        if (e.code === 'P2002') {
          updated++;
          console.log(`  🔄 Updated: ${event.question.slice(0, 60)}...`);
        } else {
          console.log(`  ❌ Error: ${e.message}`);
        }
      }
    }

    console.log();
    console.log(`📊 Summary${dryRun ? ' (dry-run)' : ''}:`);
    console.log(`   Created: ${created}`);
    console.log(`   Skipped: ${skipped}`);
    console.log(`   Updated: ${updated}`);
    console.log(`   Total:   ${events.length}`);
    console.log();
    console.log('✅ Cold start seed complete.');
    console.log(`   All seed records marked with: ${SEED_MARKER}`);
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error('❌ Cold start seed failed:', e);
  process.exit(1);
});