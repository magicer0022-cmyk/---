想法：
我想看網站（mid.syosetu.com、ncode.syosetu.com、novel18.syosetu.com）提供之PDF小說，但我不懂日文，而且PDF對於翻譯功能並不友好。
因此想出用python快速將直式PDF檔切換為橫式，再轉檔為MakeDown文件，提供進一步翻譯或處理之步驟。
我個人對於Python語言的功力僅限於以註解來檢核功能之便捷，對於修改完全苦手。
因此程式碼之產生由koboldcpp 1.122 & WOW/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf以互動方式完全授權KoboldCpp代理讀取檔案、執行並修改碼、寫入檔案、自行生成技能等方式完成程式碼之生成，即使生成程式碼極難要求正確也一次成功，需多次重置。 

用途： 
1.將PDF文件的直式文書改寫為橫向文書。 
2. 生成MakeDown檔案 
用法： 
1.PDF 檔案及pdf_vertical_to_horizo​​ntal.py 與相同資料夾。 
2.將PDF拉至pdf_vertical_to_horizo​​ntal.py 
3.PDF.mk會自動產生資料夾中。 

需求： 
安裝 python 
pip install pymupdf
