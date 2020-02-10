<center>
<h1>Fxxk baidu zip</h1>
<h4>*.fkbdz</h4>
<small>专门为了防止百度侵犯隐私而创造的整合压缩方案</small>
</center>

 third-party package needed:
 1. goto-statement
 2. pylzma
 3. demjson
 4. psutil


<h2>文件结构示例</h2>
ps:凡是''单引号括起的为在结构里的字符，其他则是名称，单引号不存在在内
整个结构在经过base64编码后存入
文件要求先压缩后加密

总文本校验'|'文件头长度'|'文件头'||'文件数据

总文本校验：sha256,检验内容：文件头长度'|'文件头'||'文件数据

文件头: 版本'|'创建时间戳(utc)'|'原文件大小'|'压缩文件大小'|'是否加密(0/1)'|'加密前sha256（若无加密则为空）'|'压缩数据sha256'|'原数据sha256


<h2>fc命令格式</h2>
{
    'mode':(str)'compress'|'decompress',(必选)
    'resource_file_path':(str)文件的oss目录,(必选)
    'save_file_path':(str)保存的oss目录,(必选)
    'password':(str)密码(非必选)
}
当password为空则以无密码执行

<h2>fc输出格式</h2>
{
    'success':(bool)true|false,
    'uuid':(str)requestID,
    'msg':(dict)返回信息
}

msg详细格式：
   1. 失败：
        {
            'errcode':(str)错误唯一代号
            'errmsg':(str)错误信息
        }
   2. 成功：
        {
            'time':(int)使用时间
            'path':(str)存储名称
            'sha256':(str)校验码
        }



<h2>错误唯一代号说明</h2>
OSSDownloadError:oss下载至服务器错误
OSSUploadError:上传至服务器错误
FileTypeError:文件格式不受支持
VerifactionError:验证失败
ParameterError:参数错误
UnknownError:未知错误
EventError:输入指令格式错误
OutOfSizeError:大小超出限制