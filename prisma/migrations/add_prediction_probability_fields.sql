-- Prediction 表加 probability / outcome / resolvedAt / brierScore
-- （§7.2 阶段0 · 0-3：所有概率玩法的硬前置）
--
-- 为什么必须做：
--   Probability 此前只存在于 PredictionFeedback（预测市场镜像表）。
--   而 Prediction 才是 1-1 概率演化追踪 / 1-3 校准曲线 / 1-2 Certified
--   Probability 三个玩法的共同底座 —— 它本体没有概率字段，三条玩法全部落不了地。
--
-- 命名约定：与 schema.prisma 一致，无 @map / @@map，PostgreSQL 直接取 camelCase 列名。
--   不要写成 snake_case —— 见 add_prediction_feedback_table.sql 里的教训
--   （snake_case DDL 曾造出并列空列，导致「11 条预测 0 条已验证」的校准飞轮空转）。
--
-- 应用方式：
--   npx prisma db push            （本地 / Vercel build）
--   或 直接对生产库执行本文件
-- 全部语句幂等，可重复执行。

ALTER TABLE "Prediction" ADD COLUMN IF NOT EXISTS "probability"  DOUBLE PRECISION;
ALTER TABLE "Prediction" ADD COLUMN IF NOT EXISTS "outcome"      TEXT;
ALTER TABLE "Prediction" ADD COLUMN IF NOT EXISTS "resolvedAt"   TIMESTAMP(3);
ALTER TABLE "Prediction" ADD COLUMN IF NOT EXISTS "brierScore"   DOUBLE PRECISION;

-- 结局取值域校验（nullable 列：IS NULL 放行）
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'Prediction_outcome_check'
    ) THEN
        ALTER TABLE "Prediction"
            ADD CONSTRAINT "Prediction_outcome_check"
            CHECK ("outcome" IS NULL OR "outcome" IN ('positive', 'negative', 'neutral'));
    END IF;
END $$;

-- 概率取值域校验（0-1）
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'Prediction_probability_check'
    ) THEN
        ALTER TABLE "Prediction"
            ADD CONSTRAINT "Prediction_probability_check"
            CHECK ("probability" IS NULL OR ("probability" >= 0 AND "probability" <= 1));
    END IF;
END $$;

-- 1-1 概率演化追踪：(userId, question) 分组后按时间排序 = 信念更新曲线
CREATE INDEX IF NOT EXISTS "Prediction_userId_question_createdAt_idx"
    ON "Prediction" ("userId", "question", "createdAt");

-- 1-3 校准曲线：按结局聚合
CREATE INDEX IF NOT EXISTS "Prediction_outcome_idx"
    ON "Prediction" ("outcome");

-- 回滚（如需）：
-- ALTER TABLE "Prediction" DROP COLUMN IF EXISTS "probability";
-- ALTER TABLE "Prediction" DROP COLUMN IF EXISTS "outcome";
-- ALTER TABLE "Prediction" DROP COLUMN IF EXISTS "resolvedAt";
-- ALTER TABLE "Prediction" DROP COLUMN IF EXISTS "brierScore";
