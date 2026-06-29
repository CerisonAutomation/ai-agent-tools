import { z } from 'zod';

/**
 * Typed schemas for all agent tool inputs and outputs.
 * Ensures predictable, validated execution across all workflows.
 */

export const BrowserInspectInput = z.object({
  url: z.string().url(),
  waitFor: z.enum(['load', 'networkidle', 'domcontentloaded']).default('networkidle'),
  extractSelectors: z.array(z.string()).optional(),
});

export const BrowserInspectOutput = z.object({
  title: z.string(),
  content: z.string(),
  extractedData: z.record(z.string()).optional(),
  timestamp: z.string().datetime(),
});

export const WebhookPayload = z.object({
  event: z.string(),
  idempotencyKey: z.string(),
  timestamp: z.string(),
  data: z.record(z.unknown()),
});

export const WorkflowResult = z.object({
  workflowId: z.string(),
  status: z.enum(['completed', 'failed', 'pending']),
  result: z.record(z.unknown()).optional(),
  error: z.string().optional(),
  executedAt: z.string().datetime(),
});

export type BrowserInspectInput = z.infer<typeof BrowserInspectInput>;
export type BrowserInspectOutput = z.infer<typeof BrowserInspectOutput>;
export type WebhookPayload = z.infer<typeof WebhookPayload>;
export type WorkflowResult = z.infer<typeof WorkflowResult>;
