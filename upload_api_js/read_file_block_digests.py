'''
运行python脚本即可获取js文件生成的fileBlockDigestList列表,不需要手动再运行js脚本
使用read_file_block_digests.py调用generatFileBlockDigest.js
'''
import subprocess
import json
import os


def run_js_script():
    try:
        # 获取当前脚本所在的目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建 generateFileBlockDigest.js 文件的路径
        js_script_path = os.path.join(script_dir, 'generateFileBlockDigest.js')
        # 使用 subprocess.run 调用 Node.js 执行 generateFileBlockDigest.js 文件
        subprocess.run(['node', js_script_path], check=True, cwd=script_dir, capture_output=True, text=True)

        # 读取生成的日志文件内容
        log_file_path = os.path.join(script_dir, 'log.txt')
        with open(log_file_path, 'r') as f:
            log_content = f.read()

        # 解析 JSON 数据
        file_block_digest_list = json.loads(log_content)
        # print(len(file_block_digest_list))
        return file_block_digest_list

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    run_js_script()
