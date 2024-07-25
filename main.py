# 获取分块上传文件信息
from upload_api_js import read_file_block_digests
import requests
import os
import base64

# 需要修改配置
access_token = 'xxx'  # 改为你的access_token
space_id = 'xxx'  # 改为你要上传文件的所属空间id
father_id = 'xxx'  # 改为你要上传文件的所属父文件夹id
filePath = r'D:\xxx\upload_api_js\upload_file'  # 改为你的路径，用于存放要上传到企微微盘的文件

# 上传文件
def upload_file_part_to_wecom(father_id):
    suc_upload = []
    fail_upload = []
    # 分块初始化上传
    init_url = f'https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload_init?access_token={access_token}'

    # 调用 run_js_script() 函数获取 file_block_digest_list
    file_block_digest_list = read_file_block_digests.run_js_script()
    # 读取分块上传文件的文件信息
    for f in file_block_digest_list:
        file_name = f["filename"]
        file_size = f["fileSize"]
        blocksha = f["blockSha"]
        blockBase64 = f["blockBase64"]

        init_data = {
            "spaceid": space_id,
            "fatherid": father_id,
            "file_name": file_name,
            "size": file_size,
            "block_sha": blocksha,
            "skip_push_card": False
        }
        init_res_data = requests.post(init_url, json=init_data).json()
        if init_res_data.get('errcode') == 0:
            upload_key = init_res_data.get('upload_key')
            file_id = init_res_data.get('fileid')

            # 没有命中秒传，将upload_key和blockBase64传给分块上传函数
            if not init_res_data.get('hit_exist'):
                file_id = upload_file_parts(upload_key, file_name, file_size, blockBase64)

            if file_id:
                print(f"{file_name}成功上传，file_id是：{file_id}")
                suc_upload.append({"file_name": file_name, "file_id": file_id})  # 添加到成功的映射
            else:
                print(f"{file_name}上传失败")
                fail_upload.append({"file_name": file_name})  # 添加到失败的映射
        else:
            print(f"{file_name}初始化上传失败: {init_res_data.get('errmsg')}")
            fail_upload.append({"file_name": file_name})  # 添加到失败的映射

    print(f"上传成功{len(suc_upload)}个：{suc_upload}，上传失败{len(fail_upload)}个：{fail_upload}")
    return suc_upload, fail_upload

def upload_file_parts(upload_key, file_name, file_size, blockBase64):
    block_num = len(blockBase64)
    chunk_size = 2097152  # 每个块的大小为2MB
    for index in range(block_num):
        # 不替换最后一块的话会报640050的错误
        if index == block_num - 1:
            # 获取最后一块file_base64_content的字节大小
            last_chunk_size = file_size - (chunk_size * index)
            print(f"{file_name}最后一块的字节大小:{last_chunk_size}")

            # 构造文件的完整路径
            full_file_path = os.path.join(filePath, file_name)
            # 将最后一块的实际字节数据转换为base64编码
            with open(full_file_path, 'rb') as f:
                f.seek(chunk_size * index)
                last_chunk_data = f.read(last_chunk_size)
                last_chunk_base64 = base64.b64encode(last_chunk_data).decode('utf-8')
                blockBase64[index] = last_chunk_base64
        # 分块上传
        part_url = f'https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload_part?access_token={access_token}'
        part_data = {
            "upload_key": upload_key,
            "index": index+1,
            "file_base64_content": blockBase64[index]
        }
        # 发送每个文件块的上传请求
        part_res_data = requests.post(part_url, json=part_data).json()
        if part_res_data.get('errcode') != 0:
            errmsg = part_res_data.get('errmsg')
            print(f"{file_name}上传文件块 {index + 1} 失败: {errmsg}")
            return
    # 分块上传完成
    file_id = finish_upload(upload_key, file_name)
    return file_id


def finish_upload(upload_key, filename):
    # 上传完成
    finish_url = f'https://qyapi.weixin.qq.com/cgi-bin/wedrive/file_upload_finish?access_token={access_token}'
    finish_data = {
        "upload_key": upload_key
    }
    finish_res_data = requests.post(finish_url, json=finish_data).json()
    if finish_res_data.get('errcode') == 0:
        file_id = finish_res_data.get('fileid')
        print(f"{filename}文件上传成功")
        return file_id
    else:
        errmsg = finish_res_data.get('errmsg')
        print(f"上传完成失败: {errmsg}")
        return


if __name__ == '__main__':
    # 上传文件到文件夹id为father_id的文件夹下
    upload_file_part_to_wecom(father_id)




