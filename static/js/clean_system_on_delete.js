/**
 * 交易系统清理脚本
 * 
 * 这个脚本添加了额外的逻辑，确保在删除所有交易对时停止交易系统
 * 使用方法：在strategy_settings.html页面加载这个脚本
 */
 
// 等待页面加载完成
document.addEventListener('DOMContentLoaded', function() {
    console.log('交易系统清理脚本已加载 - 在删除所有交易对时将自动停止系统');
    
    // 定期监控交易对数量
    setInterval(checkNoTradingPairs, 10000);
    
    // 初始检查
    setTimeout(checkNoTradingPairs, 2000);
});

/**
 * 检查交易对数量，如果没有交易对但系统仍在运行，则停止系统
 */
function checkNoTradingPairs() {
    // 只在系统运行时检查
    if (localStorage.getItem('tradingSystemRunning') !== 'true') {
        return;
    }
    
    fetch('/api/trading_pairs/list')
        .then(response => response.json())
        .then(data => {
            if (data.code === 200 && Array.isArray(data.data) && data.data.length === 0) {
                console.log('检测到没有活跃交易对，但系统仍在运行，自动停止系统');
                stopTradingSystem();
            }
        })
        .catch(error => {
            console.error('检查交易对数量时出错:', error);
        });
}

/**
 * 停止交易系统
 */
function stopTradingSystem() {
    // 清除交易系统循环
    if (window.tradingSystemInterval) {
        clearInterval(window.tradingSystemInterval);
        window.tradingSystemInterval = null;
    }
    
    // 更新系统运行状态
    localStorage.setItem('tradingSystemRunning', 'false');
    
    // 更新UI
    const runBtn = document.getElementById('run-strategy-btn');
    if (runBtn) {
        runBtn.setAttribute('data-running', 'false');
        runBtn.textContent = '运行';
        runBtn.style.backgroundColor = '#52c41a';
    }
    
    // 更新状态提示
    const statusElement = document.getElementById('strategy-status');
    if (statusElement) {
        statusElement.textContent = '交易系统已停止';
        statusElement.style.color = '#8c8c8c';
    }
    
    // 显示消息
    if (typeof showToast === 'function') {
        showToast('系统状态', '交易系统已自动停止 - 没有活跃交易对', 'info');
    } else {
        alert('交易系统已自动停止 - 没有活跃交易对');
    }
} 