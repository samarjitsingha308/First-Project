# 🔍 Search Modes - Quick Reference Card

## 🎯 Which Mode Should I Use?

### Quick Decision Tree

```
Start Here
    ↓
    Do you know the exact terms?
    ↓                    ↓
   YES                  NO
    ↓                    ↓
[KEYWORD]          Want related concepts?
                         ↓          ↓
                        YES        UNSURE
                         ↓          ↓
                    [SEMANTIC]  [HYBRID]
```

## 🔀 Mode Comparison Table

| Feature | Hybrid | Semantic | Keyword |
|---------|--------|----------|---------|
| **Best For** | General use | Exploration | Exact terms |
| **Speed** | Fast | Fast | Very fast |
| **Precision** | High | Medium | Very high |
| **Recall** | Very High | High | Medium |
| **Related Concepts** | ✅ Yes | ✅✅ Excellent | ❌ No |
| **Exact Matches** | ✅✅ Excellent | ⚠️ Sometimes | ✅✅✅ Perfect |
| **Synonyms** | ✅✅ Good | ✅✅✅ Excellent | ❌ No |
| **Technical Terms** | ✅✅ Good | ⚠️ May be broad | ✅✅✅ Perfect |

## 📊 Mode Details

### 🔀 HYBRID (Default)
```
What: Combines AI + Traditional
When: Most searches (90% of cases)
How: Adjustable 0-100% weight slider
Pro: Best of both worlds
Con: Slightly more complex
```

**Example Results:**
- Query: "Python programming"
- Finds: "Python tutorial" (keyword) + "Coding in Python" (semantic) + "Programming guide" (both)

### 🧠 SEMANTIC
```
What: AI understanding (BERT)
When: Exploring topics, unsure of terms
How: 384-dimensional embeddings
Pro: Finds related concepts
Con: May be too broad
```

**Example Results:**
- Query: "machine learning"
- Finds: "AI", "neural networks", "deep learning", "data science"

### 🔑 KEYWORD
```
What: Traditional TF-IDF
When: Exact terms known
How: Word frequency analysis
Pro: Precise, fast
Con: Misses synonyms
```

**Example Results:**
- Query: "React hooks"
- Finds: "React hooks tutorial", "Using hooks in React"
- Misses: "React functional components" (related but different words)

## ⚖️ Weight Slider Guide (Hybrid Mode)

```
┌───────────────────────────────────────┐
│  0%    25%    50%    75%    100%     │
│  ├──────┼──────┼──────┼──────┤       │
│  Keyword         ⚖️         Semantic   │
└───────────────────────────────────────┘
```

| Weight | Best For | Example Query |
|--------|----------|---------------|
| **90% Semantic** | Broad exploration | "healthy lifestyle" |
| **70% Semantic** | General (default) | "machine learning" |
| **50-50** | Balanced | "React tutorial" |
| **30% Semantic** | Specific terms | "fastapi dependency injection" |
| **10% Semantic** | Almost keyword-only | "Python 3.11 features" |

## 💡 Common Use Cases

### Research / Learning
```
Mode: Semantic or Hybrid (80%)
Why: Discover related topics
Example: "sustainable energy"
```

### Technical Documentation
```
Mode: Keyword or Hybrid (40%)
Why: Exact terminology matters
Example: "API authentication"
```

### General Information
```
Mode: Hybrid (70% - default)
Why: Balanced results
Example: "healthy recipes"
```

### Specific Code Examples
```
Mode: Keyword
Why: Exact language/framework
Example: "useState hook example"
```

## 🎯 Search Tips by Mode

### Hybrid Mode Tips
✅ Start here for most searches
✅ Adjust slider if results too broad/narrow
✅ Watch all score types
✅ Use natural language

### Semantic Mode Tips
✅ Ask questions: "How to..."
✅ Use concepts, not exact terms
✅ Try synonyms
✅ Good for brainstorming

### Keyword Mode Tips
✅ Use exact technical terms
✅ Include specific names (frameworks, tools)
✅ Use quotes for phrases (in query)
✅ Try abbreviations (ML, AI, API)

## 📈 Score Interpretation

### Hybrid Results
```
85.3% Overall    🧠 92.1%    🔑 71.5%
  ↓                ↓           ↓
Combined     Semantic    Keyword
```

**What to look for:**
- High overall = Great match
- High semantic, low keyword = Related concept
- High keyword, low semantic = Exact words, different context
- Both high = Perfect match!

### Single Mode Results
```
Semantic: 🧠 82.5%
Keyword: 🔑 91.2%
```

Simpler - just one score to consider!

## 🚦 Quick Troubleshooting

### "Too many irrelevant results"
➜ Switch to Keyword mode
➜ Or lower semantic weight in Hybrid

### "Missing obvious results"
➜ Switch to Semantic mode
➜ Or increase semantic weight in Hybrid

### "Results too technical/specific"
➜ Increase semantic weight
➜ Use more general terms

### "Results too broad/general"
➜ Decrease semantic weight
➜ Use more specific terms

## 🎓 Quick Examples

```
Query: "AI"
─────────────────────────
Hybrid:    "AI basics", "Machine Learning", "Artificial Intelligence"
Semantic:  "Deep Learning", "Neural Networks", "Data Science"
Keyword:   "AI tutorial", "AI guide", "AI introduction"
```

```
Query: "healthy food"
─────────────────────────
Hybrid:    "Nutrition guide", "Healthy eating", "Diet tips"
Semantic:  "Wellness", "Balanced diet", "Food health"
Keyword:   "Healthy food recipes", "Food for health"
```

```
Query: "web development"
─────────────────────────
Hybrid:    "Web dev guide", "Frontend coding", "Building websites"
Semantic:  "HTML CSS", "Programming websites", "Web design"
Keyword:   "Web development tutorial", "Development for web"
```

## 📱 Mobile Quick Tips

On smaller screens:
- Tap mode dropdown to switch
- Swipe slider for weight
- Scroll to see all scores
- Tap results to expand

## ⌨️ Keyboard Shortcuts

While in search box:
- `Enter` - Submit search
- `Esc` - Clear search
- (More shortcuts coming soon!)

## 🔗 Need More Info?

- **Full Guide**: Read `HYBRID_SEARCH_GUIDE.md`
- **All Features**: See `FEATURES.md`
- **Quick Start**: Check `QUICKSTART.md`
- **Troubleshooting**: Read `TROUBLESHOOTING.md`

---

**Remember**: When in doubt, use **Hybrid mode at 70%** - it's optimized for most searches! 🎯
