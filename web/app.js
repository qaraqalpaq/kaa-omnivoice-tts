const $ = (id) => document.getElementById(id);
const POLL_MS = 2000;
const SAMPLES_HINT = "Házirshe joqarıdaǵı tayın úlgilerdi tıńlap kóriń.";
const MESSAGES = {
  queue_full: `Gezek tolı. Birazdan qayta urınıp kóriń. ${SAMPLES_HINT}`,
  rate_limited: `Bir adamnan sorawlar sanı sheklengen. Shama menen {wait} keyin qayta urınıp kóriń. ${SAMPLES_HINT}`,
  empty_text: "Tekst kiritiń.",
  text_too_long: "Tekst júdá uzın.",
  unknown_voice: "Bunday dawıs joq.",
  failed: "Qátelik júz berdi. Qayta urınıp kóriń.",
};

const minutes = (s) => (s >= 60 ? `${Math.floor(s / 60)} min ${s % 60} s` : `${s} s`);

function setStatus(text, fraction) {
  $("status").hidden = false;
  $("statusText").textContent = text;
  $("progress").style.width = `${Math.round(Math.min(fraction, 1) * 100)}%`;
}

async function loadConfig() {
  const config = await (await fetch("api/config")).json();
  if (config.note) {
    $("note").textContent = config.note;
    $("note").hidden = false;
  }
  $("max").textContent = config.max_chars;
  $("text").maxLength = config.max_chars;
  $("voice").replaceChildren(...config.voices.map((v) => new Option(v.replace("kaa_voice_", "Dawıs "), v)));
  $("examples").replaceChildren(...config.examples.map((text) => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = text;
    b.onclick = () => { $("text").value = text; $("count").textContent = text.length; };
    return b;
  }));
}

async function loadSamples() {
  const response = await fetch("samples/samples.jsonl");
  if (!response.ok) return;
  const rows = (await response.text()).split("\n").filter(Boolean).map((line) => JSON.parse(line));
  const groups = new Map();
  rows.forEach((row) => groups.set(row.voice, [...(groups.get(row.voice) || []), row]));
  $("sampleGroups").replaceChildren(...[...groups].map(([voice, items], index) => {
    const group = document.createElement("details");
    group.open = index === 0;
    const title = document.createElement("summary");
    title.textContent = `${voice.replace("kaa_voice_", "Dawıs ")} · ${items.length}`;
    group.append(title, ...items.map((item) => {
      const row = document.createElement("div");
      row.className = "sample";
      const text = document.createElement("p");
      text.textContent = item.text;
      const audio = document.createElement("audio");
      audio.controls = true;
      audio.preload = "none";
      audio.src = `samples/${item.audio}`;
      row.append(text, audio);
      return row;
    }));
    return group;
  }));
  $("samples").hidden = false;
}

async function poll(id, total) {
  const job = await (await fetch(`api/jobs/${id}`)).json();
  if (job.status === "done") {
    setStatus("Tayın.", 1);
    $("player").src = job.audio_url;
    $("download").href = job.audio_url;
    $("result").hidden = false;
    $("player").play().catch(() => {});
    return true;
  }
  if (job.status === "error") throw new Error("failed");
  const label = job.status === "queued" ? `Gezekte: ${job.position}-orın` : "Islenip atır";
  setStatus(`${label} · shama menen ${minutes(job.eta_s)} qaldı`, total ? 1 - job.eta_s / total : 0);
  return false;
}

async function submit(event) {
  event.preventDefault();
  $("submit").disabled = true;
  $("result").hidden = true;
  try {
    const response = await fetch("api/speak", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: $("text").value, voice: $("voice").value, speed: Number($("speed").value) }),
    });
    const job = await response.json();
    if (!response.ok) throw Object.assign(new Error(job.detail?.code), job.detail);
    const total = Math.max(job.eta_s, 1);
    while (!(await poll(job.id, total))) await new Promise((r) => setTimeout(r, POLL_MS));
  } catch (error) {
    const message = (MESSAGES[error.message] || MESSAGES.failed).replace("{wait}", minutes(error.retry_after_s || 0));
    setStatus(message, 0);
  } finally {
    $("submit").disabled = false;
  }
}

$("text").addEventListener("input", () => { $("count").textContent = $("text").value.length; });
$("speed").addEventListener("input", () => { $("speedValue").textContent = `${Number($("speed").value).toFixed(2)}×`; });
$("form").addEventListener("submit", submit);
loadConfig();
loadSamples();
