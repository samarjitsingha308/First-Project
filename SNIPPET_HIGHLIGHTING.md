# 🎯 Snippet-Based Keyword Highlighting

## 🌟 Overview

The search engine now displays **context-aware snippets** where your keywords appear, similar to Google search results! Instead of showing truncated content, you see **relevant chunks** of text with keywords highlighted.

---

## 📸 What You'll See

### Before (Simple Highlighting)
```
Search: "machine learning"

Result:
─────────────────────────────────
Machine learning is a subset of AI that enables 
systems to learn from data. Neural networks are 
commonly used in machine learning applications...
(Shows beginning of content, may miss keywords)
```

### After (Snippet-Based) - NOW!
```
Search: "machine learning"

Result:
─────────────────────────────────
...[Machine] [learning] is a subset of AI that 
enables systems to [learn] from data...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...Neural networks are commonly used in 
[machine] [learning] applications to solve...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...Advanced [machine] [learning] algorithms can 
process complex patterns and make predictions...
(Shows multiple chunks where keywords appear!)
```

---

## ✨ Key Features

### 1. Multiple Snippets
If your keywords appear in different parts of the article, you'll see **up to 3 snippets** showing each occurrence location.

### 2. Context Around Keywords
Each snippet shows ~200 characters around the keyword, giving you context to understand relevance.

### 3. Multiple Highlights Per Snippet
If a keyword appears multiple times within the same chunk, **all occurrences are highlighted**.

### 4. Smart Chunking
- Snippets merge if keywords are close together
- Word boundaries are respected (no cut-off mid-word)
- Ellipsis (...) shows there's more text before/after

### 5. Visual Separation
Snippets are separated by dashed lines, making it easy to scan multiple matches.

---

## 🎨 Visual Example

### Search: "Python programming tutorial"

```
┌────────────────────────────────────────────────┐
│ Complete [Python] [Programming] Guide          │ ← Highlighted title
│ 92% Overall  🧠 94%  🔑 88%                   │
│                                                │
│ ...This comprehensive [Python] [programming]   │ ← Snippet 1
│ [tutorial] covers everything from basics...    │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│ ...Learn [Python] [programming] through        │ ← Snippet 2
│ hands-on examples and practical exercises...   │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│ ...Master [Python] with our step-by-step       │ ← Snippet 3
│ [tutorial] designed for beginners...           │
│                                                │
│ Matched terms: [python] [programming] [tutorial]│
└────────────────────────────────────────────────┘
```

Notice:
- 🟨 All keyword occurrences highlighted
- 📍 Multiple locations shown
- ➡️ Context around each match
- 📝 Ellipsis (...) indicates more text

---

## 🔍 How It Works

### Step-by-Step Process

1. **Find Keyword Positions**
   ```
   Content: "Python is great. Learn Python programming. Python tutorial here."
   Keywords: ["python", "programming"]
   
   Positions found:
   - "Python" at position 0
   - "Python" at position 23
   - "Python" at position 56
   - "programming" at position 30
   ```

2. **Extract Snippets**
   ```
   For each position:
   - Take 100 chars before and 100 chars after
   - Adjust to word boundaries
   - Merge if snippets overlap
   ```

3. **Create Chunks**
   ```
   Chunk 1: "Python is great. Learn Python programming..."
   Chunk 2: "...Python tutorial here and more content..."
   ```

4. **Highlight Keywords**
   ```
   Chunk 1: "[Python] is great. Learn [Python] [programming]..."
   Chunk 2: "...[Python] tutorial here and more content..."
   ```

5. **Display with Ellipsis**
   ```
   "[Python] is great. Learn [Python] [programming]..."
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   "...[Python] tutorial here and more content..."
   ```

---

## 💡 Smart Features

### Automatic Merging
```
If keywords are close together:
Position 1: chars 0-200
Position 2: chars 150-350

Result: One merged snippet (chars 0-350)
Instead of two overlapping snippets
```

### Word Boundary Detection
```
Bad:  "...arn Python prog..."
Good: "...learn Python programming..."
      └─ Starts and ends at word boundaries
```

### Snippet Limit
```
Shows up to 3 most relevant snippets
Why? Prevents overwhelming the user
Result: Most important matches shown first
```

### Ellipsis Indicators
```
Start: "..." (if snippet doesn't start at beginning)
End:   "..." (if snippet doesn't end at end)

Examples:
"Python is great..."           (more content after)
"...learn Python programming"  (more content before)
"...Python tutorial..."        (more content both sides)
```

---

## 🎯 Use Cases

### Use Case 1: Long Articles
```
Article: 5000 words about machine learning
Query: "neural networks"

Without snippets:
Shows first 300 chars (might not contain keywords)

With snippets:
Shows 3 chunks exactly where "neural networks" appears
```

### Use Case 2: Multiple Topics
```
Article: Covers Python, Java, and JavaScript
Query: "Python"

Shows only the sections discussing Python
User doesn't have to read about Java/JavaScript
```

### Use Case 3: Repeated Keywords
```
Article: "Python...Python...Python..." (keyword appears 10 times)
Query: "Python"

Shows 3 best snippets
All occurrences within those snippets are highlighted
```

---

## 📊 Snippet Display Logic

### Snippet Length
```
Default: ~200 characters per snippet
- 100 chars before keyword
- 100 chars after keyword
- Adjusted to word boundaries
```

### Number of Snippets
```
Maximum: 3 snippets per result
Why: Balance between information and readability
```

### Snippet Selection
```
1. Find all keyword positions
2. Create snippets around each position
3. Merge overlapping/nearby snippets
4. Take first 3 snippets
5. Display in order of appearance
```

---

## 🎨 Visual Styling

### Keyword Highlights
```css
Yellow gradient background
Bold text
Subtle shadow
Easy to spot at a glance
```

### Snippet Separation
```css
Dashed border between snippets
Visual breathing room
Clear chunk boundaries
```

### Ellipsis
```css
... at start/end
Indicates continuation
Subtle gray color
```

---

## 💻 Technical Implementation

### Backend (Python)

**New Method**: `_extract_keyword_snippets()`
```python
def _extract_keyword_snippets(text, keywords, snippet_length=150):
    # Find all keyword positions
    # Extract chunks around keywords
    # Merge overlapping chunks
    # Return up to 3 snippets
```

**Returns**:
```json
{
  "content_snippets": [
    {
      "start": 0,
      "end": 150,
      "text": "...snippet text..."
    },
    {
      "start": 500,
      "end": 650,
      "text": "...snippet text..."
    }
  ]
}
```

### Frontend (JavaScript)

**Snippet Display**:
```javascript
// For each snippet
content_snippets.map(snippet => {
    const prefix = snippet.start > 0 ? '...' : '';
    const suffix = snippet.end < content.length ? '...' : '';
    
    return `${prefix}${highlightedText}${suffix}`;
});
```

---

## 🔄 Fallback Behavior

### If No Keywords Found
```
Displays: First 300 characters of content
(Standard behavior)
```

### If Content is Short
```
Displays: Full content (no snippets needed)
```

### If Snippet Extraction Fails
```
Displays: Truncated content with highlights
(Graceful degradation)
```

---

## 🎯 Benefits

### For Users
✅ **See Context** - Keywords in surrounding text
✅ **Save Time** - Jump to relevant parts
✅ **Better Understanding** - Multiple contexts shown
✅ **Confirm Relevance** - See if match is meaningful

### For Search Quality
✅ **More Accurate** - Shows actual keyword usage
✅ **Less Misleading** - Don't judge by beginning only
✅ **Better Scanning** - Quick relevance assessment
✅ **Professional** - Matches commercial search UX

---

## 📝 Examples

### Example 1: Technical Article
```
Query: "async await JavaScript"

Snippet 1:
"...The [async] [await] pattern in [JavaScript] 
allows you to write asynchronous code that looks 
synchronous..."

Snippet 2:
"...When using [async] functions in [JavaScript], 
the [await] keyword pauses execution until the 
promise resolves..."

Snippet 3:
"...Modern [JavaScript] developers prefer [async]/
[await] over callbacks for cleaner code..."
```

### Example 2: Tutorial
```
Query: "beginner guide"

Snippet 1:
"...This [beginner]-friendly [guide] walks you 
through the fundamentals step by step..."

Snippet 2:
"...Perfect for [beginners], this [guide] requires 
no prior knowledge or experience..."
```

### Example 3: Multiple Keywords
```
Query: "machine learning neural networks"

Snippet 1:
"...[Machine] [learning] uses [neural] [networks] 
to identify patterns in data..."

Snippet 2:
"...Deep [learning], a subset of [machine] [learning], 
relies heavily on [neural] [networks]..."
```

---

## 🎓 Tips for Best Results

### Tip 1: Use Specific Keywords
```
Better:  "React hooks tutorial"
Result:  Shows exact sections about React hooks

Worse:   "programming"
Result:  Too many matches, less specific snippets
```

### Tip 2: Read All Snippets
```
Don't judge by first snippet only
Each snippet shows different context
All are relevant to your query
```

### Tip 3: Use Hybrid Mode
```
Hybrid mode balances semantic and keyword
Best for snippet-based display
Shows most relevant occurrences
```

---

## 🔧 Customization

### Adjust Snippet Length

Edit `search_engine.py`:
```python
# Default: 200 characters
article["content_snippets"] = self._extract_keyword_snippets(
    content, 
    article["matched_keywords"],
    snippet_length=200  # Change this
)

# Options:
# 150 - Shorter, more snippets
# 200 - Balanced (default)
# 300 - Longer, fewer snippets
```

### Change Max Snippets

Edit `search_engine.py`:
```python
# In _extract_keyword_snippets()
return merged_snippets[:3]  # Change from 3 to desired number
```

### Adjust Merge Distance

Edit `search_engine.py`:
```python
# In _extract_keyword_snippets()
elif snippet_start <= current_end + 50:  # Change 50
    # Merge if within 50 characters
```

---

## 🎉 Summary

**Snippet-based highlighting provides:**

✅ **Multiple chunks** where keywords appear
✅ **Context** around each keyword
✅ **All occurrences** highlighted within chunks
✅ **Visual separation** between snippets
✅ **Ellipsis indicators** for continuation
✅ **Smart merging** of nearby matches
✅ **Professional appearance** like Google/commercial search
✅ **Better user experience** than simple truncation

**Your search results now show exactly where and how keywords appear!** 🎯

---

**Implementation Date**: December 29, 2025  
**Feature Version**: 2.2.0  
**Status**: ✅ Complete and Active
