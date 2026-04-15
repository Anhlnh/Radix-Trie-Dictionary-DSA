import tkinter as tk
from tkinter import ttk, font as tkfont


# ══════════════════════════════════════════════════════════════
#                    PHẦN 1: RADIX TRIE
# ══════════════════════════════════════════════════════════════

class NutTrie:

    def __init__(self):
        self.children = {}
        self.nghia = None      # Nghĩa của từ (chỉ có nếu là nút kết thúc từ)
        self.la_cuoi_tu = False  # True = đây là điểm kết thúc của 1 từ hoàn chỉnh


class RadixTrie:
    
    def __init__(self):
        self.goc = NutTrie()   # Nút gốc (root), không chứa ký tự nào
        self.so_tu = 0         # Đếm số từ trong từ điển
    
    def _tien_to_chung(self, chuoi_a: str, chuoi_b: str) -> int:
        """
        Tìm độ dài tiền tố chung giữa 2 chuỗi.
        Ví dụ: "apple" và "apply" → 4 ("appl")
        """
        i = 0
        while i < len(chuoi_a) and i < len(chuoi_b) and chuoi_a[i] == chuoi_b[i]:
            i += 1
        return i
    
    def them_tu(self, tu: str, nghia: str):
        """
        Thêm 1 từ mới vào Radix Trie.
        Trả về: (True/False, thông báo)
        
        Các trường hợp xảy ra khi thêm:
        1. Không có cạnh nào khớp → tạo cạnh mới
        2. Cạnh khớp hoàn toàn → đi sâu hơn
        3. Cạnh khớp một phần → TÁCH NHÁNH (split)
        """
        tu = tu.lower().strip()
        if not tu:
            return False, "⚠️ Từ không được để trống!"
        if not tu.isalpha():
            return False, "⚠️ Từ chỉ được chứa chữ cái!"
        
        nut_hien_tai = self.goc
        phan_con_lai = tu          # Phần chữ chưa được xử lý
        
        while phan_con_lai:
            ky_tu_dau = phan_con_lai[0]
            
            # TRƯỜNG HỢP 1: Không có cạnh nào bắt đầu bằng ký tự này
            if ky_tu_dau not in nut_hien_tai.children:
                nut_moi = NutTrie()
                nut_moi.la_cuoi_tu = True
                nut_moi.nghia = nghia
                nut_hien_tai.children[ky_tu_dau] = (phan_con_lai, nut_moi)
                self.so_tu += 1
                return True, f"✅ Đã thêm '{tu}' (tạo cạnh mới '{phan_con_lai}')"
            
            # Lấy cạnh hiện có
            nhan_canh, nut_con = nut_hien_tai.children[ky_tu_dau]
            do_dai_chung = self._tien_to_chung(phan_con_lai, nhan_canh)
            
            # TRƯỜNG HỢP 2: Cạnh khớp TOÀN BỘ với nhãn cạnh
            if do_dai_chung == len(nhan_canh):
                if do_dai_chung == len(phan_con_lai):
                    # Từ kết thúc đúng tại nút này
                    if nut_con.la_cuoi_tu:
                        nut_con.nghia = nghia   # Cập nhật nghĩa
                        return True, f"🔄 Cập nhật nghĩa của '{tu}'"
                    else:
                        nut_con.la_cuoi_tu = True
                        nut_con.nghia = nghia
                        self.so_tu += 1
                        return True, f"✅ Đã thêm '{tu}'"
                else:
                    # Chưa hết từ → đi tiếp xuống dưới
                    nut_hien_tai = nut_con
                    phan_con_lai = phan_con_lai[do_dai_chung:]
                    continue
            
            # TRƯỜNG HỢP 3: Chỉ khớp MỘT PHẦN → cần TÁCH NHÁNH
            # Ví dụ: đang có cạnh 'apple', thêm 'apply'
            # → tạo cạnh 'appl', rồi 2 cạnh con 'e' và 'y'
            
            nut_giua = NutTrie()    # Nút ở điểm tách
            
            # Cạnh cũ: phần thừa sau điểm tách
            phan_cu_con_lai = nhan_canh[do_dai_chung:]
            nut_giua.children[phan_cu_con_lai[0]] = (phan_cu_con_lai, nut_con)
            
            # Cạnh mới: phần còn lại của từ đang thêm
            phan_moi_con_lai = phan_con_lai[do_dai_chung:]
            if phan_moi_con_lai:
                nut_moi = NutTrie()
                nut_moi.la_cuoi_tu = True
                nut_moi.nghia = nghia
                nut_giua.children[phan_moi_con_lai[0]] = (phan_moi_con_lai, nut_moi)
            else:
                nut_giua.la_cuoi_tu = True
                nut_giua.nghia = nghia
            
            # Thay cạnh cũ = cạnh chung mới
            phan_chung = phan_con_lai[:do_dai_chung]
            nut_hien_tai.children[ky_tu_dau] = (phan_chung, nut_giua)
            self.so_tu += 1
            return True, (f"✅ Đã thêm '{tu}' "
                         f"(tách nhánh tại '{phan_chung}' → '{phan_cu_con_lai}' & '{phan_moi_con_lai}')")
        
        # phan_con_lai rỗng → từ chính là gốc (hiếm gặp)
        if not nut_hien_tai.la_cuoi_tu:
            nut_hien_tai.la_cuoi_tu = True
            nut_hien_tai.nghia = nghia
            self.so_tu += 1
            return True, f"✅ Đã thêm '{tu}'"
        nut_hien_tai.nghia = nghia
        return True, f"🔄 Cập nhật nghĩa của '{tu}'"
    
    def tim_nghia(self, tu: str):
        """
        Tìm nghĩa của từ.
        Trả về: nghĩa (str) hoặc None nếu không tìm thấy.
        
        Độ phức tạp: O(L) với L là độ dài từ cần tìm
        """
        tu = tu.lower().strip()
        nut = self.goc
        phan_con_lai = tu
        
        while phan_con_lai:
            ky_tu_dau = phan_con_lai[0]
            if ky_tu_dau not in nut.children:
                return None  # Không tìm thấy
            
            nhan_canh, nut_con = nut.children[ky_tu_dau]
            do_dai_chung = self._tien_to_chung(phan_con_lai, nhan_canh)
            
            if do_dai_chung < len(nhan_canh):
                return None  # Từ ngắn hơn cạnh → không khớp
            
            phan_con_lai = phan_con_lai[do_dai_chung:]
            nut = nut_con
        
        return nut.nghia if nut.la_cuoi_tu else None
    
    def xoa_tu(self, tu: str):
        """
        Xóa 1 từ khỏi Radix Trie.
        Sau khi xóa sẽ dọn dẹp (gộp) các nút thừa.
        Trả về: (True/False, thông báo)
        """
        tu = tu.lower().strip()
        da_xoa, thong_bao = self._xoa_de_quy(self.goc, tu, tu)
        if da_xoa:
            self.so_tu -= 1
        return da_xoa, thong_bao
    
    def _xoa_de_quy(self, nut, phan_con_lai, tu_goc):
        """Hàm đệ quy để xóa từ và dọn dẹp cây."""
        # Đã đi đến cuối từ
        if not phan_con_lai:
            if nut.la_cuoi_tu:
                nut.la_cuoi_tu = False
                nut.nghia = None
                return True, f"✅ Đã xóa từ '{tu_goc}'"
            return False, f"❌ Không tìm thấy '{tu_goc}'"
        
        ky_tu_dau = phan_con_lai[0]
        if ky_tu_dau not in nut.children:
            return False, f"❌ Không tìm thấy '{tu_goc}'"
        
        nhan_canh, nut_con = nut.children[ky_tu_dau]
        do_dai_chung = self._tien_to_chung(phan_con_lai, nhan_canh)
        if do_dai_chung < len(nhan_canh):
            return False, f"❌ Không tìm thấy '{tu_goc}'"
        
        da_xoa, thong_bao = self._xoa_de_quy(nut_con, phan_con_lai[do_dai_chung:], tu_goc)
        
        # Dọn dẹp sau khi xóa
        if da_xoa:
            if not nut_con.la_cuoi_tu:
                so_con = len(nut_con.children)
                if so_con == 0:
                    # Nút lá không phải từ → xóa luôn
                    del nut.children[ky_tu_dau]
                elif so_con == 1:
                    # Chỉ có 1 con → gộp cạnh lại (nén)
                    duy_nhat_ky_tu = list(nut_con.children.keys())[0]
                    nhan_chau, nut_chau = nut_con.children[duy_nhat_ky_tu]
                    nhan_moi = nhan_canh + nhan_chau
                    nut.children[ky_tu_dau] = (nhan_moi, nut_chau)
        
        return da_xoa, thong_bao
    
    def lay_tat_ca_tu(self):
        """Lấy toàn bộ từ trong từ điển (sắp xếp theo ABC)."""
        ket_qua = []
        self._thu_thap(self.goc, "", ket_qua)
        return sorted(ket_qua, key=lambda x: x[0])
    
    def _thu_thap(self, nut, tien_to, ket_qua):
        """Duyệt cây để thu thập tất cả từ."""
        if nut.la_cuoi_tu:
            ket_qua.append((tien_to, nut.nghia))
        for ky_tu in sorted(nut.children.keys()):
            nhan_canh, nut_con = nut.children[ky_tu]
            self._thu_thap(nut_con, tien_to + nhan_canh, ket_qua)
    
    def ve_cay(self):
        """
        Tạo danh sách dòng hiển thị cấu trúc cây.
        
        Ví dụ output:
          🌳 ROOT (3 từ)
          ├─ 'appl'
          │   ├─ 'e'  ◉ apple → quả táo
          │   └─ 'y'  ◉ apply → áp dụng
          └─ 'book'   ◉ book → cuốn sách
        """
        cac_dong = [f"🌳 ROOT  ({self.so_tu} từ)"]
        self._ve_de_quy(self.goc, "", "", cac_dong)
        if self.so_tu == 0:
            cac_dong.append("   (Chưa có từ nào. Hãy thêm từ!)")
        return cac_dong
    
    def _ve_de_quy(self, nut, tien_to_tich_luy, la_cuoi, cac_dong):
        """Đệ quy vẽ cây."""
        danh_sach_con = sorted(nut.children.items())
        for i, (ky_tu, (nhan_canh, nut_con)) in enumerate(danh_sach_con):
            la_con_cuoi = (i == len(danh_sach_con) - 1)
            
            # Ký hiệu nhánh cây
            ky_hieu = "└─ " if la_con_cuoi else "├─ "
            thu_gan = "   " if la_con_cuoi else "│  "
            
            # Gắn nhãn nếu là cuối từ
            tu_day_du = tien_to_tich_luy + nhan_canh
            if nut_con.la_cuoi_tu:
                nghia_ngan = nut_con.nghia[:35] + "…" if len(nut_con.nghia) > 35 else nut_con.nghia
                dong = f"{la_cuoi}{ky_hieu}'{nhan_canh}'  ◉ {tu_day_du} → {nghia_ngan}"
            else:
                dong = f"{la_cuoi}{ky_hieu}'{nhan_canh}'"
            
            cac_dong.append(dong)
            self._ve_de_quy(nut_con, tu_day_du, la_cuoi + thu_gan, cac_dong)


# ══════════════════════════════════════════════════════════════
#                    PHẦN 2: GIAO DIỆN
# ══════════════════════════════════════════════════════════════

# Bảng màu (Catppuccin Mocha)
MAU = {
    "nen_chinh":   "#1e1e2e",
    "nen_panel":   "#181825",
    "nen_the":     "#313244",
    "nen_input":   "#45475a",
    "vien":        "#6c7086",
    "chu_chinh":   "#cdd6f4",
    "chu_phu":     "#a6adc8",
    "tim":         "#cba6f7",
    "xanh_duong":  "#89b4fa",
    "xanh_la":     "#a6e3a1",
    "do":          "#f38ba8",
    "vang":        "#f9e2af",
    "cam":         "#fab387",
    "hong":        "#f5c2e7",
}


class UngDungTuDien:
    def __init__(self, cua_so_goc):
        self.cua_so = cua_so_goc
        self.cua_so.title("📚 Từ Điển Tiếng Anh — Radix Trie")
        self.cua_so.geometry("1200x750")
        self.cua_so.minsize(900, 600)
        self.cua_so.configure(bg=MAU["nen_chinh"])
        
        self.trie = RadixTrie()
        self._them_du_lieu_mau()
        self._xay_giao_dien()
    
    def _them_du_lieu_mau(self):
        """Thêm sẵn một số từ mẫu để dễ thấy cấu trúc Trie."""
        du_lieu_mau = [
            ("apple",       "quả táo"),
            ("application", "ứng dụng"),
            ("apply",       "áp dụng, ứng tuyển"),
            ("appear",      "xuất hiện"),
            ("book",        "cuốn sách"),
            ("bookmark",    "đánh dấu trang"),
            ("boy",         "cậu bé"),
            ("cat",         "con mèo"),
            ("car",         "xe ô tô"),
            ("card",        "thẻ, danh thiếp"),
        ]
        for tu, nghia in du_lieu_mau:
            self.trie.them_tu(tu, nghia)
    
    def _xay_giao_dien(self):
        """Xây dựng toàn bộ giao diện."""
        self._tao_tieu_de()
        
        # Khung chứa 2 cột
        khung_chinh = tk.Frame(self.cua_so, bg=MAU["nen_chinh"])
        khung_chinh.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        # Cột trái (điều khiển)
        khung_trai = tk.Frame(khung_chinh, bg=MAU["nen_panel"], width=360)
        khung_trai.pack(side="left", fill="y", padx=(0, 12))
        khung_trai.pack_propagate(False)
        
        # Cột phải (hiển thị)
        khung_phai = tk.Frame(khung_chinh, bg=MAU["nen_chinh"])
        khung_phai.pack(side="right", fill="both", expand=True)
        
        self._tao_phan_dieu_khien(khung_trai)
        self._tao_phan_hien_thi(khung_phai)
        
        self._cap_nhat_tat_ca()
    
    def _tao_tieu_de(self):
        """Tạo phần tiêu đề."""
        khung_td = tk.Frame(self.cua_so, bg=MAU["nen_chinh"])
        khung_td.pack(fill="x", padx=16, pady=(16, 10))
        
        tk.Label(khung_td,
                 text="📚  Từ Điển Tiếng Anh",
                 font=("Arial", 22, "bold"),
                 fg=MAU["tim"], bg=MAU["nen_chinh"]).pack(side="left")
        
        tk.Label(khung_td,
                 text="  Cấu trúc dữ liệu: Radix Trie",
                 font=("Arial", 11, "italic"),
                 fg=MAU["chu_phu"], bg=MAU["nen_chinh"]).pack(side="left", pady=(8, 0))
    
    def _tao_phan_dieu_khien(self, cha):
        """Tạo cột trái: ô nhập liệu + nút bấm + danh sách từ."""
        # ── Nhập liệu ──────────────────────────────────────
        tk.Label(cha, text="✏️  Nhập từ",
                 font=("Arial", 12, "bold"),
                 fg=MAU["xanh_duong"], bg=MAU["nen_panel"]).pack(anchor="w", padx=16, pady=(18, 4))
        
        # Ô nhập từ tiếng Anh
        tk.Label(cha, text="Từ tiếng Anh:",
                 font=("Arial", 10), fg=MAU["chu_phu"], bg=MAU["nen_panel"]).pack(anchor="w", padx=16)
        
        self.bien_tu = tk.StringVar()
        o_tu = tk.Entry(cha, textvariable=self.bien_tu,
                        font=("Courier New", 13), bg=MAU["nen_input"],
                        fg=MAU["chu_chinh"], insertbackground=MAU["tim"],
                        relief="flat", bd=0)
        o_tu.pack(fill="x", padx=16, ipady=7, pady=(3, 10))
        o_tu.bind("<Return>", lambda e: self.tim_nghia())
        self.o_tu = o_tu
        
        # Ô nhập nghĩa
        tk.Label(cha, text="Nghĩa (tiếng Việt):",
                 font=("Arial", 10), fg=MAU["chu_phu"], bg=MAU["nen_panel"]).pack(anchor="w", padx=16)
        
        self.bien_nghia = tk.StringVar()
        o_nghia = tk.Entry(cha, textvariable=self.bien_nghia,
                           font=("Arial", 12), bg=MAU["nen_input"],
                           fg=MAU["chu_chinh"], insertbackground=MAU["tim"],
                           relief="flat", bd=0)
        o_nghia.pack(fill="x", padx=16, ipady=7, pady=(3, 16))
        o_nghia.bind("<Return>", lambda e: self.them_tu())
        
        # Đường kẻ ngang
        tk.Frame(cha, height=1, bg=MAU["nen_the"]).pack(fill="x", padx=16)
        
        # ── Nút bấm ────────────────────────────────────────
        tk.Label(cha, text="⚙️  Thao tác",
                 font=("Arial", 12, "bold"),
                 fg=MAU["xanh_duong"], bg=MAU["nen_panel"]).pack(anchor="w", padx=16, pady=(14, 6))
        
        nut_configs = [
            ("➕  Thêm từ",   MAU["xanh_la"], self.them_tu,
             "Thêm từ mới vào từ điển\n(Enter trong ô Nghĩa)"),
            ("🔍  Tìm nghĩa", MAU["xanh_duong"], self.tim_nghia,
             "Tìm nghĩa của từ\n(Enter trong ô Từ)"),
            ("🗑️  Xóa từ",    MAU["do"],       self.xoa_tu,
             "Xóa từ khỏi từ điển"),
            ("🗂️  Xóa trắng", MAU["vien"],     self.xoa_o_nhap,
             "Xóa nội dung ô nhập"),
        ]
        
        khung_nut = tk.Frame(cha, bg=MAU["nen_panel"])
        khung_nut.pack(fill="x", padx=16)
        
        for i, (ten, mau_nut, lenh, ghi_chu) in enumerate(nut_configs):
            nut = tk.Button(khung_nut, text=ten, command=lenh,
                            bg=mau_nut, fg=MAU["nen_chinh"],
                            font=("Arial", 10, "bold"),
                            relief="flat", cursor="hand2",
                            activebackground=mau_nut,
                            activeforeground=MAU["nen_chinh"])
            nut.pack(fill="x", pady=3, ipady=8)
            # Hiệu ứng hover
            self._hover(nut, mau_nut)
        
        # Đường kẻ ngang
        tk.Frame(cha, height=1, bg=MAU["nen_the"]).pack(fill="x", padx=16, pady=(12, 0))
        
        # ── Danh sách từ ───────────────────────────────────
        tk.Label(cha, text="📋  Danh sách từ",
                 font=("Arial", 12, "bold"),
                 fg=MAU["xanh_duong"], bg=MAU["nen_panel"]).pack(anchor="w", padx=16, pady=(10, 4))
        
        khung_ds = tk.Frame(cha, bg=MAU["nen_panel"])
        khung_ds.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        cuon = tk.Scrollbar(khung_ds, bg=MAU["nen_the"])
        cuon.pack(side="right", fill="y")
        
        self.hop_tu = tk.Listbox(khung_ds,
                                  yscrollcommand=cuon.set,
                                  bg=MAU["nen_chinh"], fg=MAU["chu_chinh"],
                                  font=("Courier New", 10),
                                  selectbackground=MAU["tim"],
                                  selectforeground=MAU["nen_chinh"],
                                  relief="flat", bd=0, activestyle="none")
        self.hop_tu.pack(fill="both", expand=True)
        cuon.config(command=self.hop_tu.yview)
        self.hop_tu.bind("<<ListboxSelect>>", self._chon_tu_danh_sach)
    
    def _tao_phan_hien_thi(self, cha):
        """Tạo cột phải: kết quả thao tác + cây Trie."""
        # ── Kết quả thao tác ───────────────────────────────
        khung_kq = tk.Frame(cha, bg=MAU["nen_panel"])
        khung_kq.pack(fill="x", pady=(0, 12))
        
        tk.Label(khung_kq, text="💬  Kết quả",
                 font=("Arial", 11, "bold"),
                 fg=MAU["vang"], bg=MAU["nen_panel"]).pack(anchor="w", padx=14, pady=(12, 4))
        
        self.nhan_kq = tk.Label(khung_kq,
                                 text="👋 Chào mừng! Đã nạp sẵn 10 từ mẫu. Hãy thử thêm hoặc tìm một từ!",
                                 font=("Arial", 11),
                                 fg=MAU["chu_chinh"], bg=MAU["nen_panel"],
                                 wraplength=750, justify="left", anchor="w")
        self.nhan_kq.pack(fill="x", padx=14, pady=(0, 12))
        
        # ── Giải thích Radix Trie ──────────────────────────
        khung_gt = tk.Frame(cha, bg=MAU["nen_the"])
        khung_gt.pack(fill="x", pady=(0, 10))
        
        huong_dan = ("ℹ️  Cách đọc sơ đồ:   "
                     "├─ / └─ = nhánh con   │   "
                     "◉ = điểm kết thúc từ hoàn chỉnh   │   "
                     "'xyz' = nhãn cạnh (chuỗi nén)")
        tk.Label(khung_gt, text=huong_dan,
                 font=("Arial", 9), fg=MAU["chu_phu"],
                 bg=MAU["nen_the"], anchor="w").pack(fill="x", padx=12, pady=6)
        
        # ── Sơ đồ cây Radix Trie ───────────────────────────
        tk.Label(cha, text="🌳  Sơ đồ Radix Trie  (cập nhật theo thời gian thực)",
                 font=("Arial", 12, "bold"),
                 fg=MAU["xanh_la"], bg=MAU["nen_chinh"]).pack(anchor="w")
        
        khung_cay = tk.Frame(cha, bg=MAU["nen_chinh"])
        khung_cay.pack(fill="both", expand=True, pady=(6, 0))
        
        cuon_ngang = tk.Scrollbar(khung_cay, orient="horizontal")
        cuon_ngang.pack(side="bottom", fill="x")
        cuon_doc = tk.Scrollbar(khung_cay)
        cuon_doc.pack(side="right", fill="y")
        
        self.van_ban_cay = tk.Text(khung_cay,
                                    font=("Courier New", 11),
                                    bg=MAU["nen_panel"], fg=MAU["chu_chinh"],
                                    xscrollcommand=cuon_ngang.set,
                                    yscrollcommand=cuon_doc.set,
                                    state="disabled", relief="flat",
                                    wrap="none", padx=14, pady=10,
                                    cursor="arrow")
        self.van_ban_cay.pack(fill="both", expand=True)
        cuon_ngang.config(command=self.van_ban_cay.xview)
        cuon_doc.config(command=self.van_ban_cay.yview)
        
        # Màu sắc cho từng loại dòng
        self.van_ban_cay.tag_config("goc",     foreground=MAU["tim"],        font=("Courier New", 12, "bold"))
        self.van_ban_cay.tag_config("cuoi_tu", foreground=MAU["xanh_la"])
        self.van_ban_cay.tag_config("nhanh",   foreground=MAU["xanh_duong"])
        self.van_ban_cay.tag_config("trong",   foreground=MAU["chu_phu"],    font=("Courier New", 10, "italic"))
    
    # ══════════════════════════════════════════════════════
    #              CÁC HÀM XỬ LÝ THAO TÁC
    # ══════════════════════════════════════════════════════
    
    def them_tu(self):
        """Xử lý khi bấm nút Thêm từ."""
        tu = self.bien_tu.get().strip()
        nghia = self.bien_nghia.get().strip()
        
        if not tu:
            self._hien_kq("⚠️  Vui lòng nhập từ tiếng Anh!", MAU["vang"])
            self.o_tu.focus()
            return
        if not nghia:
            self._hien_kq("⚠️  Vui lòng nhập nghĩa của từ!", MAU["vang"])
            return
        
        thanh_cong, thong_bao = self.trie.them_tu(tu, nghia)
        mau = MAU["xanh_la"] if thanh_cong else MAU["cam"]
        self._hien_kq(thong_bao, mau)
        
        self.bien_tu.set("")
        self.bien_nghia.set("")
        self.o_tu.focus()
        self._cap_nhat_tat_ca()
    
    def tim_nghia(self):
        """Xử lý khi bấm nút Tìm nghĩa."""
        tu = self.bien_tu.get().strip()
        if not tu:
            self._hien_kq("⚠️  Nhập từ cần tìm vào ô bên trên!", MAU["vang"])
            self.o_tu.focus()
            return
        
        nghia = self.trie.tim_nghia(tu)
        if nghia:
            self.bien_nghia.set(nghia)
            self._hien_kq(f"🔍  Tìm thấy   '{tu}'  →  {nghia}", MAU["xanh_duong"])
        else:
            self.bien_nghia.set("")
            self._hien_kq(f"❌  Không tìm thấy '{tu}' trong từ điển. Hãy thêm từ này!", MAU["do"])
    
    def xoa_tu(self):
        """Xử lý khi bấm nút Xóa từ."""
        tu = self.bien_tu.get().strip()
        if not tu:
            self._hien_kq("⚠️  Nhập từ cần xóa vào ô bên trên!", MAU["vang"])
            self.o_tu.focus()
            return
        
        da_xoa, thong_bao = self.trie.xoa_tu(tu)
        mau = MAU["do"] if da_xoa else MAU["cam"]
        self._hien_kq(thong_bao, mau)
        
        if da_xoa:
            self.bien_tu.set("")
            self.bien_nghia.set("")
        self._cap_nhat_tat_ca()
    
    def xoa_o_nhap(self):
        """Xóa nội dung các ô nhập."""
        self.bien_tu.set("")
        self.bien_nghia.set("")
        self._hien_kq("🗂️  Đã xóa nội dung ô nhập.", MAU["chu_phu"])
        self.o_tu.focus()
    
    def _chon_tu_danh_sach(self, event):
        """Khi click vào 1 từ trong danh sách → điền vào ô nhập."""
        chon = self.hop_tu.curselection()
        if chon:
            tat_ca = self.trie.lay_tat_ca_tu()
            vi_tri = chon[0]
            if vi_tri < len(tat_ca):
                tu, nghia = tat_ca[vi_tri]
                self.bien_tu.set(tu)
                self.bien_nghia.set(nghia)
                self._hien_kq(f"📌  Đã chọn '{tu}' từ danh sách. Có thể xóa hoặc cập nhật!", MAU["hong"])
    
    # ══════════════════════════════════════════════════════
    #              HÀM CẬP NHẬT GIAO DIỆN
    # ══════════════════════════════════════════════════════
    
    def _cap_nhat_tat_ca(self):
        """Cập nhật danh sách từ và sơ đồ cây."""
        self._cap_nhat_danh_sach()
        self._cap_nhat_so_do_cay()
    
    def _cap_nhat_danh_sach(self):
        """Làm mới danh sách từ bên trái."""
        self.hop_tu.delete(0, "end")
        tat_ca = self.trie.lay_tat_ca_tu()
        for tu, nghia in tat_ca:
            hien_thi = f"  {tu:<18} {nghia}"
            self.hop_tu.insert("end", hien_thi)
    
    def _cap_nhat_so_do_cay(self):
        """Vẽ lại sơ đồ Radix Trie."""
        cac_dong = self.trie.ve_cay()
        
        self.van_ban_cay.config(state="normal")
        self.van_ban_cay.delete("1.0", "end")
        
        for dong in cac_dong:
            if "ROOT" in dong:
                self.van_ban_cay.insert("end", dong + "\n", "goc")
            elif "◉" in dong:
                self.van_ban_cay.insert("end", dong + "\n", "cuoi_tu")
            elif dong.strip().startswith("("):
                self.van_ban_cay.insert("end", dong + "\n", "trong")
            else:
                self.van_ban_cay.insert("end", dong + "\n", "nhanh")
        
        self.van_ban_cay.config(state="disabled")
    
    def _hien_kq(self, thong_bao: str, mau: str):
        """Hiển thị kết quả thao tác."""
        self.nhan_kq.config(text=thong_bao, fg=mau)
    
    def _hover(self, nut: tk.Button, mau_goc: str):
        """Thêm hiệu ứng hover cho nút."""
        def vao(_):
            nut.config(bg=self._lam_sang(mau_goc))
        def ra(_):
            nut.config(bg=mau_goc)
        nut.bind("<Enter>", vao)
        nut.bind("<Leave>", ra)
    
    def _lam_sang(self, mau_hex: str) -> str:
        """Làm sáng màu hex lên một chút."""
        mau_hex = mau_hex.lstrip("#")
        r, g, b = int(mau_hex[0:2], 16), int(mau_hex[2:4], 16), int(mau_hex[4:6], 16)
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"


# ══════════════════════════════════════════════════════════════
#                    KHỞI ĐỘNG ỨNG DỤNG
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    cua_so = tk.Tk()
    ung_dung = UngDungTuDien(cua_so)
    
    cua_so.update_idletasks()
    rong = cua_so.winfo_width()
    cao = cua_so.winfo_height()
    x = (cua_so.winfo_screenwidth() // 2) - (rong // 2)
    y = (cua_so.winfo_screenheight() // 2) - (cao // 2)
    cua_so.geometry(f"{rong}x{cao}+{x}+{y}")
    
    cua_so.mainloop()