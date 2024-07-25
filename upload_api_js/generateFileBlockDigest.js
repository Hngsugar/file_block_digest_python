const fs = require('fs');
const { resolve } = require("path");
const { generateFileBlockDigest } = require(".");

const folderPath = './upload_file'; // 定义需要分块上传文件的所属文件夹
const logFilePath = './log.txt'; // 日志文件路径


const run = async () => {
  try{
    // 读取文件夹中的所有文件, 定义一个列表来存储每个文件的fileBlockDigest对象
    const files = fs.readdirSync(folderPath);
    const fileBlockDigestList = [];


    // 遍历每个文件并生成文件块摘要
    for (const file of files) {
      // 使用 resolve 函数构建每个文件的完整路径
      const filePath = resolve(folderPath, file);
      const fileBlockDigest = await generateFileBlockDigest(filePath);

      // 在文件块摘要对象中加入文件名属性
      fileBlockDigest.filename = file;
      fileBlockDigestList.push(fileBlockDigest);
    }
    console.log('len:', fileBlockDigestList.length);
    // 将日志信息写入日志文件
    const logContent = JSON.stringify(fileBlockDigestList, null, 2); // 格式化 JSON 输出
    fs.writeFileSync(logFilePath, logContent);

    console.log(`Log file written successfully: ${logFilePath}`);

  } catch (err) {
    console.error('Error reading folder:', err);
  }
};

run();
