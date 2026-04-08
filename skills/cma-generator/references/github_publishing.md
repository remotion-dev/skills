# GitHub Pages Publishing

This document covers how to publish CMA HTML reports to `https://graehamwatts.github.io/cma-reports/`. There are two methods — the API method (preferred, fast) and the browser editor fallback (if the token expires).

---

## Method 1: GitHub API via Browser (Preferred)

This is the fastest approach. It uses a GitHub Personal Access Token (PAT) to push files via the GitHub Contents API, called from the browser using `javascript_tool`. The sandbox proxy blocks `api.github.com`, so the API call must be made from the browser, which is on the user's machine and has direct internet access.

### Prerequisites

- A GitHub Fine-Grained PAT with Contents: Read and Write permission on the `cma-reports` repo
- Claude in Chrome browser tools available
- Any tab open in the browser (doesn't matter which page)

### The Token

```
YOUR_GITHUB_PAT_HERE
```

If this token has expired, ask the user to generate a new one at https://github.com/settings/tokens. The token needs:
- Repository access: "Only select repositories" → `cma-reports`
- Permissions: Contents → "Read and write"

### Step 1: Base64 Encode the HTML

In the sandbox, base64 encode the finished HTML file:

```python
import base64

with open('CMA_file.html', 'rb') as f:
    html_data = f.read()

b64_content = base64.b64encode(html_data).decode('ascii')

with open('b64_content.txt', 'w') as f:
    f.write(b64_content)

print(f"Original: {len(html_data)} bytes -> Base64: {len(b64_content)} chars")
```

### Step 2: Transfer Base64 to Browser

The base64 content is ~138KB for a typical CMA, which needs to be transferred in chunks via javascript_tool (~3500 chars per call = ~40 chunks). Split and transfer:

```bash
split -b 3500 b64_content.txt b64_
```

Then transfer each chunk:
```javascript
// First chunk
window._b64 = '<chunk_aa contents>';
'c1: ' + window._b64.length

// Subsequent chunks
window._b64 += '<chunk_ab contents>';
'c2: ' + window._b64.length
```

**Optimization tip**: To reduce chunks from ~40 to ~7, compress first with raw deflate:
```python
import zlib, base64
with open('CMA_file.html', 'rb') as f:
    html_data = f.read()
compressed = zlib.compress(html_data, 9)[2:-4]  # Raw deflate: strip zlib header + checksum
b64_content = base64.b64encode(compressed).decode('ascii')
```
Then decompress in the browser before the API call (see "Compression Optimization" section at the end).

### Step 3: Push via API

Once all content is in `window._b64`, make the API call. For a new file:

```javascript
// Check if file already exists (to get SHA for updates)
const TOKEN = 'YOUR_GITHUB_PAT_HERE';
const FILENAME = 'CMA_789_Green_Street.html';

fetch('https://api.github.com/repos/Graehamwatts/cma-reports/contents/' + FILENAME, {
  headers: {
    'Authorization': 'Bearer ' + TOKEN,
    'Accept': 'application/vnd.github+json'
  }
}).then(r => r.ok ? r.json() : null).then(existing => {
  const body = {
    message: 'Add CMA report for [full street address]',
    content: window._b64
  };
  // If file exists, include SHA to update it
  if (existing && existing.sha) body.sha = existing.sha;

  return fetch('https://api.github.com/repos/Graehamwatts/cma-reports/contents/' + FILENAME, {
    method: 'PUT',
    headers: {
      'Authorization': 'Bearer ' + TOKEN,
      'Accept': 'application/vnd.github+json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
}).then(r => r.json()).then(data => {
  window._commitResult = data;
  return data.content ? 'SUCCESS! SHA: ' + data.content.sha + ' Size: ' + data.content.size : 'FAILED: ' + JSON.stringify(data).substring(0, 200);
}).catch(e => 'Error: ' + e.message);
```

**Important**: The `content` field must be the raw base64 of the HTML file — NOT the compressed version. If you used compression to transfer fewer chunks, you must decompress in the browser first and then re-encode with `btoa()` before making the API call.

### Step 4: Verify

GitHub Pages deploys within 1-2 minutes. Check the live URL with a cache-busting param:
```
https://graehamwatts.github.io/cma-reports/CMA_[address].html?v=2
```

### Error Handling

| Error | Meaning | Fix |
|-------|---------|-----|
| 403 "Resource not accessible" | Token lacks write permission | Generate new token with Contents: Read and write |
| 409 "SHA doesn't match" | File was modified since you fetched the SHA | Re-fetch the current SHA and retry |
| 422 "content is not valid Base64" | Content wasn't properly base64 encoded | Check encoding — must be standard base64, no URL-safe variant |

---

## Method 2: Browser Editor Fallback

If the API token has expired and the user can't immediately create a new one, use the GitHub web editor. This was the original method used for Bradley Way, Bayshore, and 789 Green Street.

### Overview

1. Compress HTML with raw deflate (~100KB → ~18KB)
2. Base64 encode (~18KB → ~24KB)
3. Split into ~3500 char chunks (~7 chunks)
4. Navigate to `https://github.com/Graehamwatts/cma-reports/edit/main/CMA_[address].html` (or `/new/main?filename=...` for new files)
5. Transfer chunks via javascript_tool to `window._b64`
6. Decompress in browser using `DecompressionStream('deflate-raw')`
7. Insert into CodeMirror editor:
   ```javascript
   const cm = document.querySelector('.cm-content');
   cm.focus();
   document.execCommand('selectAll', false, null);
   document.execCommand('insertText', false, window._decompressedHtml);
   ```
8. Click "Commit changes..." → set message → click "Commit changes" in dialog

### Key Details for Browser Method

- CodeMirror 6 virtualizes rendering — `cm.textContent` only shows visible lines. Check gutter line count to verify full content.
- The decompression uses async `DecompressionStream('deflate-raw')` — javascript_tool returns `undefined` for async code. Follow up with a separate check: `window._decompressedHtml ? 'Ready' : 'Not yet'`
- Use `document.execCommand` for insertion, NOT `cmView.view.dispatch` (the view property path varies).
- For the commit message input, use the native value setter to trigger React state updates.

---

## Compression Optimization (for either method)

When using compression to reduce transfer chunks:

```python
# In sandbox: compress with raw deflate
import zlib, base64
compressed = zlib.compress(html_data, 9)[2:-4]
b64_compressed = base64.b64encode(compressed).decode('ascii')
# ~100KB HTML → ~24KB base64 (7 chunks instead of 40)
```

```javascript
// In browser: decompress
const binary = atob(window._b64);
const bytes = new Uint8Array(binary.length);
for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);

const ds = new DecompressionStream('deflate-raw');
const writer = ds.writable.getWriter();
writer.write(bytes);
writer.close();

const reader = ds.readable.getReader();
const chunks = [];
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  chunks.push(value);
}
const totalLen = chunks.reduce((a, c) => a + c.length, 0);
const merged = new Uint8Array(totalLen);
let offset = 0;
for (const c of chunks) { merged.set(c, offset); offset += c.length; }

const html = new TextDecoder().decode(merged);

// For API method: re-encode as base64 for the API call
window._b64 = btoa(html);
```

## Key Numbers

- **javascript_tool practical limit**: ~3500 chars per call
- **Typical CMA HTML size**: ~100KB (2300+ lines)
- **Uncompressed base64**: ~138KB → ~40 chunks
- **Compressed base64**: ~24KB → ~7 chunks
- **API method total calls**: 7 transfer + 1 decompress + 1 re-encode + 1 API push = ~10 calls
- **Browser editor total calls**: 7 transfer + 1 decompress + 5 editor/commit steps = ~14 calls
