// Ask an open LLM a question in Arabic or English.
// Node 18+ (built-in fetch), no dependencies. Same endpoint settings as chat.py.
//
//   node chat.mjs "What is a foundation model?"
//   node chat.mjs "ما هو النموذج التأسيسي؟"

const BASE_URL = process.env.LLM_BASE_URL ?? "http://localhost:11434/v1";
const MODEL = process.env.LLM_MODEL ?? "qwen2.5:3b";
const API_KEY = process.env.LLM_API_KEY ?? "not-needed-for-local";

const SYSTEM =
  "You are a helpful assistant for students and developers in the UAE. " +
  "Answer in the same language as the question (Arabic or English), " +
  "in plain words, in at most five sentences.";

const question =
  process.argv.slice(2).join(" ") ||
  "ما هو النموذج التأسيسي؟ اشرحه لطالب في المرحلة الثانوية.";

const start = performance.now();
const response = await fetch(`${BASE_URL}/chat/completions`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${API_KEY}`,
  },
  body: JSON.stringify({
    model: MODEL,
    messages: [
      { role: "system", content: SYSTEM },
      { role: "user", content: question },
    ],
    temperature: 0.3,
  }),
});

if (!response.ok) {
  console.error(`Request failed: ${response.status} ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
console.log(data.choices[0].message.content.trim());
const seconds = ((performance.now() - start) / 1000).toFixed(2);
console.error(
  `\n[${MODEL} | ${seconds} s | ${data.usage?.completion_tokens ?? "?"} output tokens]`
);
