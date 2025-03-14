import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing import layout, pymupdf
import os
from pypdf import PdfWriter  # 替换 PdfMerger 为 PdfWriter

target = "E:/lab/python/pyqt/output/ls/target"
result = "E:/lab/python/pyqt/output/ls/result"

# 确保 result 目录存在
if not os.path.exists(result):
    os.makedirs(result)

ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#FFFFFF"

# PDF creation
file_names = []
file_paths = []
for file in os.listdir(target):
    file_names.append(file.split(" ")[0])  # 提取文件名部分
    file_paths.append(os.path.join(target, file))

print("Files found in target directory:")
for fp in file_paths:
    print(fp)

for i, file_path in enumerate(file_paths):
    try:
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        backend = pymupdf.PyMuPdfBackend()
        Frontend(RenderContext(doc), backend).draw_layout(msp)
        res_file = os.path.join(result, file_names[i] + ".pdf")
        with open(res_file, "wb") as fp:
            fp.write(backend.get_pdf_bytes(layout.Page(0, 0)))
        print(res_file)
        print("PDF ready " + str(i + 1) + "/" + str(len(file_names)))
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("PDFs creation completed!")

# PDF merging
pdf_paths = []
writer = PdfWriter()  # 使用 PdfWriter 替代 PdfMerger
res_pdf_file = os.path.join(result, "output.pdf")

# 获取所有 PDF 文件路径
for pdf in os.listdir(result):
    if pdf.endswith(".pdf"):  # 确保只处理 PDF 文件
        pdf_paths.append(os.path.join(result, pdf))

print("PDFs to merge:")
for pp in pdf_paths:
    print(pp)

# 合并 PDF
for i, pdf_path in enumerate(pdf_paths):
    print(pdf_path)
    writer.append(pdf_path)  # 使用 append 方法
    print("ready " + str(i + 1) + "/" + str(len(pdf_paths)))

# 写入合并后的文件
writer.write(res_pdf_file)
writer.close()

print("PDF merging completed!")
