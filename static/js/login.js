document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const mobileInput = document.getElementById('mobile');
    const passwordInput = document.getElementById('password');
    const rememberMeCheckbox = document.getElementById('remember-me');
    const loginBtn = document.getElementById('login-btn');
    const forgotLink = document.querySelector('.forgot-link');
    const registerLink = document.querySelector('.register-link a');
    
    // 可选：预填充测试账号，方便用户测试
    const testAccountBtn = document.querySelector('.test-account-tip');
    if (testAccountBtn) {
        testAccountBtn.style.cursor = 'pointer';
        testAccountBtn.addEventListener('click', function() {
            mobileInput.value = '13602958586';
            passwordInput.value = 'abcd8312';
        });
    }
    
    // 检查本地存储中是否有保存的账号信息
    const savedMobile = localStorage.getItem('rememberedMobile');
    if (savedMobile) {
        mobileInput.value = savedMobile;
        rememberMeCheckbox.checked = true;
    }
    
    // 验证手机号格式
    function isValidMobile(mobile) {
        return /^1[3-9]\d{9}$/.test(mobile);
    }
    
    // 登录按钮点击事件
    loginBtn.addEventListener('click', function() {
        const mobile = mobileInput.value.trim();
        const password = passwordInput.value;
        
        // 表单验证
        if (!isValidMobile(mobile)) {
            alert('请输入正确的手机号码');
            mobileInput.focus();
            return;
        }
        
        if (password.length < 6) {
            alert('密码长度至少为6位');
            passwordInput.focus();
            return;
        }
        
        // 保存记住的手机号
        if (rememberMeCheckbox.checked) {
            localStorage.setItem('rememberedMobile', mobile);
        } else {
            localStorage.removeItem('rememberedMobile');
        }
        
        // 构建登录数据
        const loginData = {
            mobile: mobile,
            password: password
        };
        
        // 发送登录请求
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.code === 200) {
                window.location.href = '/dashboard';
            } else {
                alert(data.message || '登录失败，请检查账号和密码');
            }
        })
        .catch(error => {
            console.error('登录请求失败:', error);
            alert('网络错误，请稍后重试');
        });
    });
    
    // 回车键提交表单
    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loginBtn.click();
        }
    });
    
    // 忘记密码链接点击事件
    forgotLink.addEventListener('click', function(e) {
        e.preventDefault();
        alert('忘记密码功能暂未开放');
    });
}); 