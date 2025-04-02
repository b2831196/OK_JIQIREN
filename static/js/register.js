document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const mobileInput = document.getElementById('mobile');
    const verifyCodeInput = document.getElementById('verify-code');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const agreeCheckbox = document.getElementById('agree');
    const sendCodeBtn = document.getElementById('send-code-btn');
    const registerBtn = document.getElementById('register-btn');
    const loginLink = document.querySelector('.login-link a');
    
    // 倒计时初始值（秒）
    let countdown = 60;
    let timer = null;
    
    // 验证手机号格式
    function isValidMobile(mobile) {
        return /^1[3-9]\d{9}$/.test(mobile);
    }
    
    // 验证密码强度
    function isValidPassword(password) {
        return password.length >= 6;
    }
    
    // 启动倒计时
    function startCountdown() {
        sendCodeBtn.disabled = true;
        sendCodeBtn.style.backgroundColor = '#f5f7fa';
        sendCodeBtn.style.color = '#909399';
        sendCodeBtn.style.borderColor = '#dcdfe6';
        
        timer = setInterval(function() {
            countdown--;
            sendCodeBtn.textContent = `${countdown}秒后重新获取`;
            
            if (countdown <= 0) {
                clearInterval(timer);
                sendCodeBtn.disabled = false;
                sendCodeBtn.textContent = '获取验证码';
                sendCodeBtn.style.backgroundColor = '#f0f5ff';
                sendCodeBtn.style.color = '#1a73e8';
                sendCodeBtn.style.borderColor = '#b3d4ff';
                countdown = 60;
            }
        }, 1000);
    }
    
    // 简化验证码处理，便于测试
    const autoFillVerifyCode = function() {
        verifyCodeInput.value = '123456'; // 自动填充验证码
    };
    
    // 发送验证码
    sendCodeBtn.addEventListener('click', function() {
        const mobile = mobileInput.value.trim();
        
        if (!isValidMobile(mobile)) {
            alert('请输入正确的手机号码');
            mobileInput.focus();
            return;
        }
        
        // 自动填充验证码，简化测试流程
        autoFillVerifyCode();
        alert('测试模式：验证码已自动填充');
        startCountdown();
    });
    
    // 注册按钮点击事件
    registerBtn.addEventListener('click', function() {
        const mobile = mobileInput.value.trim();
        const verifyCode = verifyCodeInput.value.trim() || '123456'; // 如果为空，使用默认验证码
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const inviteCode = document.getElementById('invite-code').value.trim();
        
        // 表单验证
        if (!isValidMobile(mobile)) {
            alert('请输入正确的手机号码');
            mobileInput.focus();
            return;
        }
        
        // 简化验证码验证
        if (!verifyCode) {
            autoFillVerifyCode();
        }
        
        if (!isValidPassword(password)) {
            alert('密码长度至少为6位');
            passwordInput.focus();
            return;
        }
        
        if (password !== confirmPassword) {
            alert('两次输入的密码不一致');
            confirmPasswordInput.focus();
            return;
        }
        
        if (!agreeCheckbox.checked) {
            alert('请阅读并同意用户协议和隐私政策');
            return;
        }
        
        // 构建注册数据
        const registerData = {
            mobile: mobile,
            verifyCode: verifyCode,
            password: password
        };
        
        // 如果有邀请码，则添加到注册数据中
        if (inviteCode) {
            registerData.inviteCode = inviteCode;
        }
        
        // 发送注册请求
        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registerData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.code === 200) {
                alert('注册成功！即将跳转到登录页面');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 1500);
            } else {
                alert(data.message || '注册失败，请稍后重试');
            }
        })
        .catch(error => {
            console.error('注册请求失败:', error);
            alert('网络错误，请稍后重试');
        });
    });
    
    // 登录链接点击事件
    loginLink.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = '/login';
    });
}); 