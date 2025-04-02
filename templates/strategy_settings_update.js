/**
 * 策略设置页面的功能增强
 * 在页面加载时自动运行，添加交易对管理和循环下单功能
 */

// 等待文档加载完成
document.addEventListener('DOMContentLoaded', function() {
    console.log('策略设置页面功能增强已加载');
    
    // 查找运行策略按钮
    const runBtn = document.getElementById('run-strategy-btn');
    if (!runBtn) {
        console.error('未找到运行策略按钮');
        return;
    }
    
    // 创建一个新的按钮替换原有按钮，以移除原有的事件监听
    const newRunBtn = runBtn.cloneNode(true);
    runBtn.parentNode.replaceChild(newRunBtn, runBtn);
    
    // 为新按钮添加事件监听
    newRunBtn.addEventListener('click', function() {
        const isRunning = newRunBtn.getAttribute('data-running') === 'true';
        
        // 获取当前表单数据
        const tradePairInput = document.getElementById('selected-crypto-pair');
        const tradePair = tradePairInput ? tradePairInput.value : 'BTC-USDT';
        
        const marginInput = document.getElementById('margin-input');
        const marginValue = marginInput ? marginInput.value : '0';
        
        const directionInput = document.querySelector('input[name="trade-direction"]:checked');
        const tradeDirection = directionInput ? directionInput.value : 'buy';
        
        // 验证保证金
        if (!isRunning && (!marginValue || parseFloat(marginValue) <= 0)) {
            showToast('请输入有效的保证金金额', 'warning');
            return;
        }
        
        if (isRunning) {
            // 正在运行，需要停止循环下单
            stopOrderLoop();
            
            // 更新按钮状态
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
        } else {
            // 未运行，需要先检查是否已添加交易对
            checkTradingPairsExists(function(hasTradingPairs, pairsData) {
                if (hasTradingPairs) {
                    // 有交易对，询问是否清理并添加新的
                    const confirmMsg = '检测到已有交易对，运行前需要清理现有交易对并添加新的。是否继续？';
                    if (confirm(confirmMsg)) {
                        // 确认后启动策略
                        runStrategyWithCleanup(tradePair, marginValue, tradeDirection);
                    }
                } else {
                    // 没有交易对，先添加一个再启动
                    const confirmMsg = '您需要先添加交易对才能启动策略。是否添加当前设置的交易对并启动？';
                    if (confirm(confirmMsg)) {
                        // 直接添加并启动
                        addTradingPairOnly(tradePair, marginValue, tradeDirection, function(success) {
                            if (success) {
                                // 添加成功后启动
                                setTimeout(function() {
                                    runStrategyWithCleanup(tradePair, marginValue, tradeDirection);
                                }, 500); // 短暂延时确保交易对保存完成
                            }
                        });
                    } else {
                        showToast('请先添加交易对后再启动策略', 'info');
                    }
                }
            });
        }
    });
    
    // 添加一个新的"添加交易对"按钮
    if (!document.getElementById('add-pair-btn')) {
        const addPairBtn = document.createElement('button');
        addPairBtn.id = 'add-pair-btn';
        addPairBtn.className = 'btn-primary';
        addPairBtn.style.backgroundColor = '#1890ff';
        addPairBtn.style.color = 'white';
        addPairBtn.style.border = 'none';
        addPairBtn.style.borderRadius = '4px';
        addPairBtn.style.padding = '8px 16px';
        addPairBtn.style.marginRight = '10px';
        addPairBtn.innerHTML = '<i class="fas fa-plus" style="margin-right: 5px;"></i> 添加交易对';
        
        // 在运行按钮前面添加此按钮
        newRunBtn.parentNode.insertBefore(addPairBtn, newRunBtn);
        
        // 添加事件监听
        addPairBtn.addEventListener('click', function() {
            // 获取当前表单数据
            const tradePairInput = document.getElementById('selected-crypto-pair');
            const tradePair = tradePairInput ? tradePairInput.value : 'BTC-USDT';
            
            const marginInput = document.getElementById('margin-input');
            const marginValue = marginInput ? marginInput.value : '0';
            
            const directionInput = document.querySelector('input[name="trade-direction"]:checked');
            const direction = directionInput ? directionInput.value : 'buy';
            
            // 验证数据
            if (!marginValue || parseFloat(marginValue) <= 0) {
                showToast('请输入有效的保证金金额', 'warning');
                return;
            }
            
            // 使用新函数添加交易对
            addTradingPairOnly(tradePair, marginValue, direction, function(success, data) {
                if (success) {
                    // 成功添加后，更新交易对列表（如果页面有显示列表）
                    if (typeof refreshTradingPairs === 'function') {
                        refreshTradingPairs();
                    }
                }
            });
        });
        
        console.log('成功添加"添加交易对"按钮');
    }
    
    // 添加清理按钮（如果页面中没有）
    if (!document.getElementById('cleanup-pairs-btn')) {
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
        
        // 在运行按钮后面添加清理按钮
        newRunBtn.parentNode.insertBefore(cleanupBtn, newRunBtn.nextSibling);
        
        // 添加事件监听
        cleanupBtn.addEventListener('click', function() {
            if (confirm('确定要清理所有交易对吗？这将停止所有正在运行的策略。')) {
                cleanupAllTradingPairs();
                
                // 同时停止循环
                stopOrderLoop();
                
                // 更新按钮状态
                newRunBtn.setAttribute('data-running', 'false');
                newRunBtn.textContent = '运行';
                newRunBtn.style.backgroundColor = '#52c41a';
                
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
    
    // 检查初始运行状态
    const isRunning = localStorage.getItem('tradingSystemRunning') === 'true';
    if (isRunning) {
        // 从本地存储获取之前的配置
        const savedTradePair = localStorage.getItem('activeTradePair') || tradePairInput.value || 'BTC-USDT';
        const savedMarginValue = localStorage.getItem('activeMarginValue') || marginInput.value || '0';
        const savedDirection = localStorage.getItem('activeDirection') || 'buy';
        
        // 检查交易对是否仍然存在
        checkTradingPairsExists(function(hasTradingPairs) {
            if (hasTradingPairs) {
                // 有交易对，恢复运行状态
                newRunBtn.setAttribute('data-running', 'true');
                newRunBtn.textContent = '停止';
                newRunBtn.style.backgroundColor = '#ff4d4f';
                
                // 更新状态提示
                const statusElement = document.getElementById('strategy-status');
                if (statusElement) {
                    statusElement.textContent = `交易系统运行中 - 交易对: ${savedTradePair}，保证金: ${savedMarginValue} USDT`;
                    statusElement.style.color = '#52c41a';
                }
                
                // 恢复循环下单
                startOrderLoop(savedTradePair, savedMarginValue, savedDirection);
                
                console.log('检测到有效的交易对和运行状态，已恢复循环下单');
            } else {
                // 没有交易对，重置运行状态
                localStorage.setItem('tradingSystemRunning', 'false');
                newRunBtn.setAttribute('data-running', 'false');
                newRunBtn.textContent = '运行';
                newRunBtn.style.backgroundColor = '#52c41a';
                
                // 更新状态提示
                const statusElement = document.getElementById('strategy-status');
                if (statusElement) {
                    statusElement.textContent = '交易系统未运行，请先添加交易对后再启动';
                    statusElement.style.color = '#8c8c8c';
                }
                
                console.log('检测到无效的交易对，已重置运行状态');
                
                // 提示用户
                showToast('未检测到交易对，请先添加交易对后再启动策略', 'warning');
            }
        });
    } else {
        // 检查是否有交易对，但未在运行中
        checkTradingPairsExists(function(hasTradingPairs, pairsData) {
            const statusElement = document.getElementById('strategy-status');
            if (statusElement) {
                if (hasTradingPairs) {
                    // 有交易对但未运行
                    statusElement.textContent = '已添加交易对，可以启动策略';
                    statusElement.style.color = '#1890ff';
                    console.log('检测到已添加交易对，但策略未运行');
                } else {
                    // 没有交易对
                    statusElement.textContent = '交易系统未运行，请先添加交易对后再启动';
                    statusElement.style.color = '#8c8c8c';
                    console.log('检测到未添加交易对，策略未运行');
                }
            }
        });
    }
    
    console.log('已完成运行策略按钮和清理按钮的事件绑定');
});

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

// 启动循环下单
function startOrderLoop(tradePair, marginValue, direction) {
    console.log(`启动循环下单: ${tradePair}, ${marginValue} USDT, 方向: ${direction}`);
    
    // 先清除可能存在的旧定时器
    if (window.orderLoopInterval) {
        clearInterval(window.orderLoopInterval);
        console.log('已清除旧的循环下单定时器');
    }
    
    // 立即检查交易对并执行一次下单
    checkTradingPairsExists(function(hasTradingPairs) {
        if (hasTradingPairs) {
            executeOrder(tradePair, marginValue, direction);
        } else {
            console.warn('未检测到交易对，无法执行下单');
            showToast('未检测到交易对，无法执行下单', 'warning');
            
            // 更新状态
            const statusElement = document.getElementById('strategy-status');
            if (statusElement) {
                statusElement.textContent = '交易系统异常：未检测到交易对，已停止运行';
                statusElement.style.color = '#ff4d4f';
            }
            
            // 重置运行状态
            stopOrderLoop();
            const runBtn = document.getElementById('new-run-btn');
            if (runBtn) {
                runBtn.setAttribute('data-running', 'false');
                runBtn.textContent = '运行';
                runBtn.style.backgroundColor = '#52c41a';
            }
            localStorage.setItem('tradingSystemRunning', 'false');
            return;
        }
    });
    
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
        
        // 先检查交易对是否存在
        checkTradingPairsExists(function(hasTradingPairs) {
            if (!hasTradingPairs) {
                console.warn('循环检测到交易对不存在，停止循环');
                showToast('检测到交易对已被移除，停止循环下单', 'error');
                
                // 更新状态
                const statusElement = document.getElementById('strategy-status');
                if (statusElement) {
                    statusElement.textContent = '交易系统异常：检测到交易对已被移除，已停止运行';
                    statusElement.style.color = '#ff4d4f';
                }
                
                // 重置运行状态
                stopOrderLoop();
                const runBtn = document.getElementById('new-run-btn');
                if (runBtn) {
                    runBtn.setAttribute('data-running', 'false');
                    runBtn.textContent = '运行';
                    runBtn.style.backgroundColor = '#52c41a';
                }
                localStorage.setItem('tradingSystemRunning', 'false');
                return;
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

// 运行策略前的完整流程
function runStrategyWithCleanup(tradePair, marginValue, direction) {
    // 首先检查是否有交易对
    checkTradingPairsExists(function(hasTradingPairs) {
        if (!hasTradingPairs) {
            // 没有交易对，显示提示消息
            showToast('未检测到交易对，请先添加交易对后再启动策略', 'warning');
            return;
        }
        
        // 有交易对，继续执行清理和重新保存流程
        // 1. 清理现有交易对
        cleanupAllTradingPairs(function(data) {
            // 2. 保存新的交易对到后端
            saveTradingPair(tradePair, marginValue, function(saveData) {
                if (saveData && saveData.code === 200) {
                    // 3. 启动循环下单
                    startOrderLoop(tradePair, marginValue, direction);
                    
                    // 4. 设置运行状态
                    const runBtn = document.getElementById('new-run-btn');
                    if (runBtn) {
                        runBtn.setAttribute('data-running', 'true');
                        runBtn.textContent = '停止';
                        runBtn.style.backgroundColor = '#ff4d4f';
                    }
                    
                    // 更新状态提示
                    const statusElement = document.getElementById('strategy-status');
                    if (statusElement) {
                        statusElement.textContent = `交易系统运行中 - 交易对: ${tradePair}，保证金: ${marginValue} USDT`;
                        statusElement.style.color = '#52c41a';
                    }
                    
                    // 保存运行状态和当前配置到localStorage
                    localStorage.setItem('tradingSystemRunning', 'true');
                    localStorage.setItem('activeTradePair', tradePair);
                    localStorage.setItem('activeMarginValue', marginValue);
                    localStorage.setItem('activeDirection', direction);
                    
                    console.log(`已启动循环下单，交易对: ${tradePair}，保证金: ${marginValue} USDT，方向: ${direction}`);
                } else {
                    // 保存交易对失败
                    showToast('保存交易对失败，无法启动策略', 'error');
                    console.error('保存交易对失败:', saveData);
                }
            });
        });
    });
}

// 只添加交易对，不启动策略
function addTradingPairOnly(tradePair, marginValue, direction, callback) {
    // 验证输入
    if (!tradePair || !marginValue || parseFloat(marginValue) <= 0) {
        showToast('请确保交易对和保证金金额有效', 'warning');
        if (typeof callback === 'function') {
            callback(false);
        }
        return;
    }
    
    // 保存交易对到后端
    saveTradingPair(tradePair, marginValue, function(saveData) {
        if (saveData && saveData.code === 200) {
            // 成功添加
            showToast(`交易对 ${tradePair} 已成功添加，保证金: ${marginValue} USDT`, 'success');
            
            // 更新状态提示
            const statusElement = document.getElementById('strategy-status');
            if (statusElement) {
                statusElement.textContent = '已添加交易对，可以启动策略';
                statusElement.style.color = '#1890ff';
            }
            
            if (typeof callback === 'function') {
                callback(true, saveData);
            }
        } else {
            // 添加失败
            showToast('添加交易对失败，请稍后再试', 'error');
            console.error('添加交易对失败:', saveData);
            
            if (typeof callback === 'function') {
                callback(false, saveData);
            }
        }
    });
} 