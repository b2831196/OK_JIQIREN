
        // 持仓更新通知脚本 - 自动生成于 2025-03-29 20:10:20
        localStorage.setItem('okxPositionCount', '0');
        localStorage.setItem('okxPositionsUpdateTime', '1743250220680');
        
        // 如果页面已加载，立即更新UI
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            if (typeof updateGlobalPositionStatus === 'function') {
                updateGlobalPositionStatus(0);
            }
            
            // 触发自定义事件
            window.dispatchEvent(new CustomEvent('okxPositionUpdated', {
                detail: { count: 0 }
            }));
        }
    