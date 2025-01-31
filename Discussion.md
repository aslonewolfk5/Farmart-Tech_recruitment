Implementation

# Solutions Considered

## 1. Binary Search Approach
- **Assumption**: Logs are sorted
- **Pros**: Fast search (O(log n))
- **Cons**: Not suitable for unsorted data

## 2. Full File Scan
- **Pros**: Works with unsorted data
- **Cons**: Slow (O(n)), high memory usage

## 3. Indexing Solution (Chosen)
- **Pros**:
  - Handles unsorted logs
  - Efficient with memory mapping
  - Fast subsequent searches
  - Scales for large files (1TB)
- **Cons**: Initial index creation time

# Final Solution Summary

### Why Indexing Solution?
- **Handles Unsorted Data**: Works regardless of log order
- **Memory Efficient**: Uses mmap for large files
- **Fast Searches**: Index allows quick retrieval
- **Scalable**: Suitable for 1TB file size

### Key Components
- **Memory Mapping**: Efficient file access
- **Index Structure**: Quick log retrieval
- **Chunk Processing**: Manages large files
- **Progress Tracking**: Monitors indexing

# Steps to Run

1. **Setup Directories**:
```bash
mkdir -p src output
```

2. **Place Log File**:
Ensure `logs_2024.log` is in the project root.

3. **Run Extraction**:
Execute the script to retrieve logs for a specific date.

4. **Check Results**:
- Output file: `output/output_YYYY-MM-DD.txt`
- Progress shown in terminal
- Error messages for any issues

