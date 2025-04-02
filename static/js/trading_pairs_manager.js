/**
 * 交易对管理工具
 * 提供交易对的清理、保存和循环下单功能
 */

// 清理所有交易对
function cleanupAllTradingPairs(callback) {
    console.log('开始清理所有交易对...');
    showToast('正在清理交易对...', 'info');
    
    // 显示加载指示器
    if (typeof showLoading === 'function') {
        showLoading();
    }
    
    // 调用后端API清理交易对
    fetch('/api/position/close', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            instId: 'ALL', // 特殊标记，表示清理所有
            posSide: 'ALL'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('交易对清理结果:', data);
        
        // 隐藏加载指示器
        if (typeof hideLoading === 'function') {
            hideLoading();
        }
        
        if (data.code === 200) {
            showToast('交易对清理成功!', 'success');
        } else {
            showToast(`交易对清理失败: ${data.message}`, 'error');
        }
        
        // 回调函数
        if (typeof callback === 'function') {
            callback(data);
        }
    })
    .catch(error => {
        console.error('清理交易对出错:', error);
        
        // 隐藏加载指示器
        if (typeof hideLoading === 'function') {
            hideLoading();
        }
        
        showToast('清理交易对时出错，请稍后再试', 'error');
        
        // 回调函数
        if (typeof callback === 'function') {
            callback(null, error);
        }
    });
}

// 保存交易对到后端
function saveTradingPair(tradePair, marginValue, callback) {
    console.log(`正在保存交易对 ${tradePair}，保证金 ${marginValue}...`);
    
    // 显示加载指示器
    if (typeof showLoading === 'function') {
        showLoading();
    }
    
    // 发送请求到后端添加交易对
    fetch('/api/strategy/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            strategyId: '1', // 默认使用策略ID 1
            marginValue: marginValue,
            tradePair: tradePair,
            tradeDirection: 'buy', // 默认做多
            saveOnly: true // 只保存，不下单
        })
    })
    .then(response => response.json())
    .then(data => {
        // 隐藏加载指示器
        if (typeof hideLoading === 'function') {
            hideLoading();
        }
        
        if (data.code === 200) {
            console.log(`交易对 ${tradePair} 已保存到后端`);
            showToast(`交易对 ${tradePair} 已保存`, 'success');
        } else {
            console.error(`保存交易对 ${tradePair} 失败:`, data.message);
            showToast(`保存交易对失败: ${data.message}`, 'error');
        }
        
        // 回调函数
        if (typeof callback === 'function') {
            callback(data);
        }
    })
    .catch(error => {
        console.error('保存交易对出错:', error);
        
        // 隐藏加载指示器
        if (typeof hideLoading === 'function') {
            hideLoading();
        }
        
        showToast('保存交易对时出错，请稍后再试', 'error');
        
        // 回调函数
        if (typeof callback === 'function') {
            callback(null, error);
        }
    });
}

// 启动循环下单
function startOrderLoop(tradePair, marginValue, direction) {
    console.log(`启动循环下单: ${tradePair}, ${marginValue} USDT, 方向: ${direction}`);
    
    // 先清除可能存在的旧定时器
    if (window.orderLoopInterval) {
        clearInterval(window.orderLoopInterval);
        console.log('已清除旧的循环下单定时器');
    }
    
    // 立即执行一次下单
    executeOrder(tradePair, marginValue, direction);
    
    // 设置新的定时器，定期执行下单操作
    window.orderLoopInterval = setInterval(function() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        console.log(`[${timeString}] 执行循环下单...`);
        
        // 更新最后检查时间
        const lastCheckElement = document.getElementById('last-refresh-time');
        if (lastCheckElement) {
            lastCheckElement.textContent = `上次检查时间: ${timeString}`;
        }
        
        // 检查系统是否允许下单
        fetch('/api/system/status')
            .then(response => response.json())
            .then(data => {
                if (data.code === 200 && data.allow_placing_orders) {
                    // 系统允许下单，执行下单操作
                    executeOrder(tradePair, marginValue, direction);
                } else {
                    console.log('系统当前不允许下单，跳过本次循环');
                }
            })
            .catch(error => {
                console.error('检查系统状态失败:', error);
            });
    }, 60000); // 每60秒执行一次
    
    console.log('已启动循环下单，间隔为60秒');
    return window.orderLoopInterval;
}

// 停止循环下单
function stopOrderLoop() {
    if (window.orderLoopInterval) {
        clearInterval(window.orderLoopInterval);
        window.orderLoopInterval = null;
        console.log('已停止循环下单');
        return true;
    }
    return false;
}

// 执行下单
function executeOrder(tradePair, marginValue, direction) {
    console.log(`执行下单: ${tradePair}, ${marginValue} USDT, 方向: ${direction}`);
    
    // 发送请求保存策略并下单
    fetch('/api/strategy/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            strategyId: '1', // 默认使用策略ID 1
            marginValue: marginValue,
            tradePair: tradePair,
            tradeDirection: direction
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            // 下单成功
            if (data.orderResult) {
                console.log('下单成功，订单信息:', data.orderResult);
                // 显示toast消息而不是对话框，避免干扰用户
                showToast(`下单成功: ${tradePair}, ${data.orderResult.contractSize}张`, 'success');
            } else {
                console.log('请求成功，但没有订单结果');
            }
        } else {
            // 下单失败
            console.error('下单失败:', data.message);
            showToast(`下单失败: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        console.error('下单出错:', error);
        showToast('下单时出错，请稍后再试', 'error');
    });
}

// 运行策略前的完整流程
function runStrategyWithCleanup(tradePair, marginValue, direction) {
    // 1. 清理现有交易对
    cleanupAllTradingPairs(function(data) {
        // 2. 保存新的交易对到后端
        saveTradingPair(tradePair, marginValue, function(saveData) {
            if (saveData && saveData.code === 200) {
                // 3. 启动循环下单
                startOrderLoop(tradePair, marginValue, direction);
                
                // 4. 设置运行状态
                const runBtn = document.getElementById('run-strategy-btn');
                if (runBtn) {
                    runBtn.setAttribute('data-running', 'true');
                    runBtn.textContent = '停止';
                    runBtn.style.backgroundColor = '#ff4d4f';
                }
                
                // 更新状态提示
                const statusElement = document.getElementById('strategy-status');
                if (statusElement) {
                    statusElement.textContent = '交易系统正在运行中...';
                    statusElement.style.color = '#52c41a';
                }
                
                // 保存运行状态到localStorage
                localStorage.setItem('tradingSystemRunning', 'true');
            }
        });
    });
}

// 检查是否已添加交易对
function checkTradingPairsExists(callback) {
    fetch('/api/trading_pairs/list')
        .then(response => response.json())
        .then(data => {
            if (data.code === 200 && Array.isArray(data.data)) {
                const hasTradingPairs = data.data.length > 0;
                if (typeof callback === 'function') {
                    callback(hasTradingPairs, data.data);
                }
            } else {
                if (typeof callback === 'function') {
                    callback(false, []);
                }
            }
        })
        .catch(error => {
            console.error('检查交易对失败:', error);
            if (typeof callback === 'function') {
                callback(false, []);
            }
        });
}

// 导出一个初始化函数，用于添加事件监听器
function initTradingPairsManager() {
    console.log('初始化交易对管理器...');
    
    // 等待DOM加载完成
    document.addEventListener('DOMContentLoaded', function() {
        // 1. 为运行策略按钮添加增强的事件监听
        const runStrategyBtn = document.getElementById('run-strategy-btn');
        if (runStrategyBtn) {
            // 移除原有事件监听（如果有）
            const newRunBtn = runStrategyBtn.cloneNode(true);
            runStrategyBtn.parentNode.replaceChild(newRunBtn, runStrategyBtn);
            
            // 添加新的事件监听
            newRunBtn.addEventListener('click', function() {
                // 获取当前表单数据
                const tradePairInput = document.getElementById('selected-crypto-pair');
                const tradePair = tradePairInput ? tradePairInput.value : 'BTC-USDT';
                
                const marginInput = document.getElementById('margin-input');
                const marginValue = marginInput ? marginInput.value : '0';
                
                // 获取交易方向
                const directionElement = document.querySelector('.type-active');
                const tradeDirection = directionElement && directionElement.textContent === '做多' ? 'buy' : 'sell';
                
                // 验证数据
                if (!marginValue || parseFloat(marginValue) <= 0) {
                    showToast('请输入有效的保证金金额', 'warning');
                    return;
                }
                
                // 检查是否已运行
                const isRunning = newRunBtn.getAttribute('data-running') === 'true';
                if (isRunning) {
                    // 正在运行，需要停止
                    if (stopOrderLoop()) {
                        newRunBtn.setAttribute('data-running', 'false');
                        newRunBtn.textContent = '运行';
                        newRunBtn.style.backgroundColor = '#52c41a';
                        
                        // 更新状态提示
                        const statusElement = document.getElementById('strategy-status');
                        if (statusElement) {
                            statusElement.textContent = '交易系统已停止';
                            statusElement.style.color = '#8c8c8c';
                        }
                        
                        // 保存运行状态到localStorage
                        localStorage.setItem('tradingSystemRunning', 'false');
                        
                        showToast('交易系统已停止', 'info');
                    }
                } else {
                    // 未运行，需要启动
                    // 先检查是否有现有交易对，如果有则需要清理
                    checkTradingPairsExists(function(hasTradingPairs) {
                        if (hasTradingPairs) {
                            // 有现有交易对，显示确认对话框
                            if (confirm('检测到已有交易对，运行前需要清理。是否继续？')) {
                                runStrategyWithCleanup(tradePair, marginValue, tradeDirection);
                            }
                        } else {
                            // 没有现有交易对，直接添加并启动
                            runStrategyWithCleanup(tradePair, marginValue, tradeDirection);
                        }
                    });
                }
            });
            
            console.log('成功为运行按钮添加交易对管理逻辑');
        }
        
        // 2. 添加清理按钮（如果页面中没有）
        if (!document.getElementById('cleanup-pairs-btn')) {
            const strategyButton = document.getElementById('run-strategy-btn');
            if (strategyButton && strategyButton.parentNode) {
                const cleanupBtn = document.createElement('button');
                cleanupBtn.id = 'cleanup-pairs-btn';
                cleanupBtn.className = 'btn-warning';
                cleanupBtn.style.backgroundColor = '#faad14';
                cleanupBtn.style.color = 'white';
                cleanupBtn.style.border = 'none';
                cleanupBtn.style.borderRadius = '4px';
                cleanupBtn.style.padding = '8px 16px';
                cleanupBtn.style.marginLeft = '10px';
                cleanupBtn.innerHTML = '<i class="fas fa-broom" style="margin-right: 5px;"></i> 清理交易对';
                
                strategyButton.parentNode.insertBefore(cleanupBtn, strategyButton.nextSibling);
                
                // 添加事件监听
                cleanupBtn.addEventListener('click', function() {
                    if (confirm('确定要清理所有交易对吗？这将停止所有正在运行的策略。')) {
                        cleanupAllTradingPairs();
                        
                        // 同时停止循环
                        stopOrderLoop();
                        
                        // 更新按钮状态
                        const currentRunBtn = document.getElementById('run-strategy-btn');
                        if (currentRunBtn) {
                            currentRunBtn.setAttribute('data-running', 'false');
                            currentRunBtn.textContent = '运行';
                            currentRunBtn.style.backgroundColor = '#52c41a';
                        }
                        
                        // 更新状态提示
                        const statusElement = document.getElementById('strategy-status');
                        if (statusElement) {
                            statusElement.textContent = '交易系统已停止，交易对已清理';
                            statusElement.style.color = '#8c8c8c';
                        }
                        
                        // 保存运行状态到localStorage
                        localStorage.setItem('tradingSystemRunning', 'false');
                    }
                });
                
                console.log('成功添加清理交易对按钮');
            }
        }
        
        // 3. 检查初始运行状态
        const isRunning = localStorage.getItem('tradingSystemRunning') === 'true';
        const initialRunBtn = document.getElementById('run-strategy-btn');
        if (initialRunBtn && isRunning) {
            initialRunBtn.setAttribute('data-running', 'true');
            initialRunBtn.textContent = '停止';
            initialRunBtn.style.backgroundColor = '#ff4d4f';
            
            // 更新状态提示
            const statusElement = document.getElementById('strategy-status');
            if (statusElement) {
                statusElement.textContent = '交易系统正在运行中...';
                statusElement.style.color = '#52c41a';
            }
            
            console.log('检测到系统应该处于运行状态，已更新UI');
        }
    });
}

// 自动初始化
initTradingPairsManager(); 