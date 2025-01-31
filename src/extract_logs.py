import sys
import os
from datetime import datetime
import mmap
from typing import Dict, List
import tempfile

class LogProcessor:
    def __init__(self, chunk_size: int = 1024 * 1024):  # 1MB chunks
        self.chunk_size = chunk_size
        self.index: Dict[str, List[int]] = {}
        
    def create_index(self, input_file: str) -> None:
        print("Creating index for faster searches...")
        with open(input_file, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            file_size = len(mm)
            processed = 0
            pos = 0
            
            while pos < file_size:
                if processed % (100 * 1024 * 1024) == 0:  # Show progress every 100MB
                    print(f"Indexing: {processed // (1024 * 1024)}MB / {file_size // (1024 * 1024)}MB")
                    
                line_end = mm.find(b'\n', pos)
                if line_end == -1:
                    line_end = file_size
                    
                try:
                    line = mm[pos:line_end].decode('utf-8')
                    date = line[:10]
                    if date not in self.index:
                        self.index[date] = []
                    self.index[date].append(pos)
                except:
                    pass
                
                processed += line_end - pos
                pos = line_end + 1
            
            mm.close()
    
    def extract_logs(self, input_file: str, target_date: str) -> int:
        if not self.index:
            self.create_index(input_file)
            
        output_file = f"output/output_{target_date}.txt"
        count = 0
        
        if target_date in self.index:
            print(f"Found {len(self.index[target_date])} potential matches. Extracting...")
            
            with open(input_file, 'rb') as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                
                with open(output_file, 'w') as out:
                    for pos in self.index[target_date]:
                        line_end = mm.find(b'\n', pos)
                        if line_end == -1:
                            line_end = len(mm)
                            
                        try:
                            line = mm[pos:line_end].decode('utf-8')
                            if line[:10] == target_date:  # Double check date
                                out.write(line + '\n')
                                count += 1
                        except:
                            pass
                            
                mm.close()
        
        return count

def validate_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def create_output_dir():
    os.makedirs('output', exist_ok=True)

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)
        
    target_date = sys.argv[1]
    
    try:
        validate_date(target_date)
        create_output_dir()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(os.path.dirname(script_dir), 'logs_2024.log')
        
        if not os.path.exists(log_file):
            raise FileNotFoundError(f"Log file not found: {log_file}")
            
        processor = LogProcessor()
        count = processor.extract_logs(log_file, target_date)
        
        print(f"\nExtracted {count} logs for {target_date}")
        print(f"Results saved to output/output_{target_date}.txt")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()