#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV去重并分割工具
读取txt文件中的CSV数据，去除完全相同的行，然后分割成多个文件
大文件不建议使用，会一次性加载到内存里
"""

import os
import traceback


def deduplicate_and_split_csv(input_file, output_dir=None, split_count=10, include_header=True, encoding='utf-8'):
    """
    去除CSV文件中的重复行，并分割成多个文件
    
    Args:
        input_file: 输入文件路径
        output_dir: 输出目录，如果为None则使用输入文件所在目录
        split_count: 分割成多少个文件
        include_header: 是否在每个分割文件中包含首行（表头）
        encoding: 文件编码，默认utf-8
    """
    # 参数校验
    if split_count <= 0:
        print("错误: split_count 必须大于 0")
        return
    
    if output_dir is None:
        output_dir = os.path.dirname(input_file) or '.'
    
    # 获取文件名（不含扩展名）和扩展名
    base_name = os.path.basename(input_file)
    name_without_ext, ext = os.path.splitext(base_name)
    
    try:
        # 读取所有行
        with open(input_file, 'r', encoding=encoding) as f:
            lines = f.readlines()
        
        original_count = len(lines)
        print(f"原始行数: {original_count}")
        
        # 去重（保持顺序）
        seen = set()
        unique_lines = []
        duplicate_count = 0
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and line_stripped not in seen:
                seen.add(line_stripped)
                unique_lines.append(line_stripped)
            elif line_stripped:
                duplicate_count += 1
        
        unique_count = len(unique_lines)
        print(f"去重后行数: {unique_count}")
        print(f"删除重复行: {duplicate_count}")
        
        # 处理首行（表头）
        header = None
        data_lines = unique_lines
        
        if include_header and unique_lines:
            header = unique_lines[0]
            data_lines = unique_lines[1:]
            print(f"首行作为表头: {header[:50]}..." if len(header) > 50 else f"首行作为表头: {header}")
        
        # 计算每个文件的行数
        total_data = len(data_lines)
        if total_data == 0:
            print("警告: 没有数据可分割")
            return
        
        # 计算基础行数和需要多分配一行的文件数
        base_lines_per_file = total_data // split_count
        extra_lines = total_data % split_count
        
        print(f"\n分割配置:")
        print(f"  - 分割份数: {split_count}")
        print(f"  - 数据总行数: {total_data}")
        print(f"  - 每份基础行数: {base_lines_per_file}")
        print(f"  - 有 {extra_lines} 个文件会多1行")
        
        # 分割并写入文件
        current_index = 0
        output_files = []
        
        for i in range(split_count):
            # 前 extra_lines 个文件多分配一行
            lines_for_this_file = base_lines_per_file + (1 if i < extra_lines else 0)
            
            if lines_for_this_file == 0:
                continue
            
            # 获取当前文件的数据
            file_data = data_lines[current_index:current_index + lines_for_this_file]
            current_index += lines_for_this_file
            
            # 生成输出文件名
            output_file = os.path.join(output_dir, f"{name_without_ext}_part{i+1:03d}{ext}")
            output_files.append(output_file)
            
            # 写入文件
            with open(output_file, 'w', encoding=encoding) as f:
                if include_header and header:
                    f.write(header + '\n')
                for line in file_data:
                    f.write(line + '\n')
            
            actual_lines = len(file_data) + (1 if include_header and header else 0)
            print(f"  创建: {os.path.basename(output_file)} ({actual_lines} 行)")
        
        print(f"\n完成! 共创建 {len(output_files)} 个文件")
        print(f"输出目录: {output_dir}")
        
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {input_file}")
    except PermissionError:
        print(f"错误: 没有读写权限 - {input_file} 或 {output_dir}")
    except UnicodeDecodeError:
        print(f"错误: 文件编码不是 {encoding}，请检查文件编码或指定正确的 encoding 参数")
    except Exception as e:
        print(f"错误: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    # ============ 配置区域 ============
    
    # 输入文件路径
    input_file = "filtered_records.txt"
    
    # 输出目录（None表示使用输入文件所在目录）
    output_dir = None
    
    # 分割成多少份
    split_count = 10
    
    # 文件编码
    encoding = 'utf-8'
    
    # 是否在每个分割文件中包含首行（表头）
    # True: 每个文件都包含首行（首行会从数据中分离出来）
    # False: 首行作为普通数据处理，不特殊对待
    include_header = True
    
    # ============ 执行 ============
    print("开始去重并分割...")
    print("=" * 50)
    deduplicate_and_split_csv(
        input_file=input_file,
        output_dir=output_dir,
        split_count=split_count,
        include_header=include_header,
        encoding=encoding
    )
    print("=" * 50)
    print("处理完成!")
