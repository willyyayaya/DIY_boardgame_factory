// 當文檔加載完成後執行
document.addEventListener('DOMContentLoaded', function() {
    // 表單驗證函數
    function validateForm() {
        // 獲取Select2元素
        const themesSelect = document.getElementById('themes');
        const mechanicsSelect = document.getElementById('mechanics');
        
        // 如果這些元素存在，進行驗證
        if (themesSelect && mechanicsSelect) {
            // 表單提交事件
            const form = document.getElementById('preferencesForm');
            if (form) {
                form.addEventListener('submit', function(e) {
                    let valid = true;
                    
                    // 驗證主題至少選擇一個
                    if (!themesSelect.value || themesSelect.value.length === 0) {
                        document.getElementById('themes-error').classList.remove('hidden');
                        valid = false;
                    } else {
                        document.getElementById('themes-error').classList.add('hidden');
                    }
                    
                    // 驗證機制至少選擇一個
                    if (!mechanicsSelect.value || mechanicsSelect.value.length === 0) {
                        document.getElementById('mechanics-error').classList.remove('hidden');
                        valid = false;
                    } else {
                        document.getElementById('mechanics-error').classList.add('hidden');
                    }
                    
                    if (!valid) {
                        e.preventDefault();
                    }
                });
            }
        }
    }
    
    // 打印按鈕功能
    const printButton = document.getElementById('printButton');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // 初始化表單驗證
    validateForm();
    
    // 如果頁面上有Select2元素，進行初始化
    if (typeof jQuery !== 'undefined' && typeof jQuery.fn.select2 !== 'undefined') {
        jQuery('.select2-multiple').select2({
            placeholder: '請選擇（可多選）',
            allowClear: true,
            language: {
                noResults: function() {
                    return '沒有找到匹配項';
                }
            }
        });
    }
}); 