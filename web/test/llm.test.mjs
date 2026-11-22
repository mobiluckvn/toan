/**
 * VỎ GỌI MÔ HÌNH (`functions/src/llm.js`) — canh mấy chỗ Gemini khác Groq.
 * Không cần mạng lẫn khoá: chỉ soi gói sẽ gửi và đường nới khuôn.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  soanGoi, laLoiKhuon, goiDoiJson, TOKEN_SAN, MO_HINH,
} from '../functions/src/llm.js';

test('mô hình mặc định là Gemini 3.8 Flash', () => {
  assert.equal(MO_HINH, process.env.LLM_MODEL || 'gemini-3.8-flash');
});

test('gói gửi: bỏ temperature, nâng trần token, mặc định nghĩ ít', () => {
  const g = soanGoi({ model: 'm', messages: [{ role: 'user', content: 'x' }],
    temperature: 0.2, max_tokens: 200 });
  assert.equal('temperature' in g, false);
  assert.equal(g.max_tokens, TOKEN_SAN);
  assert.equal(g.reasoning_effort, 'low');
});

test('gói chỉ có lời dặn thì thêm một lượt user — Gemini bác gói không có nội dung', () => {
  const g = soanGoi({ messages: [{ role: 'system', content: 'dặn' }] });
  assert.equal(g.messages.length, 2);
  assert.equal(g.messages[1].role, 'user');
  const h = soanGoi({ messages: [{ role: 'system', content: 'd' }, { role: 'user', content: 'u' }] });
  assert.equal(h.messages.length, 2);
});

test('nhận ra lỗi khuôn của cả Groq lẫn Gemini, không nhận nhầm khoá sai', () => {
  assert.ok(laLoiKhuon({ status: 400, error: { error: { code: 'json_validate_failed' } } }));
  assert.ok(laLoiKhuon({ status: 400, message: 'response_format is not supported with tools' }));
  assert.ok(!laLoiKhuon({ status: 401, message: 'json' }));
});

test('bị bác vì khuôn thì nới ĐÚNG một lần, bỏ response_format', async () => {
  const da = [];
  const client = { chat: { completions: { create: async (p) => {
    da.push(p);
    if (p.response_format) {
      const e = new Error('json_validate_failed'); e.status = 400; throw e;
    }
    return { choices: [{ message: { content: '{"a":1}' } }] };
  } } } };
  const kq = await goiDoiJson(client, { model: 'm', messages: [] });
  assert.equal(da.length, 2);
  assert.equal(da[1].response_format, undefined);
  assert.equal(kq.choices[0].message.content, '{"a":1}');
});
