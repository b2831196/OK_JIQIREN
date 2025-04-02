// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化菜单点击事件
    initMenuItems();
    
    // 初始化创建机器人按钮
    initCreateRobotButton();
    
    // 初始化添加机器人卡片
    initAddRobotCard();
    
    // 初始化机器人卡片按钮
    initRobotCardButtons();
    
    // 初始化刷新按钮事件
    initRefreshButton();
});

// 初始化菜单点击事件
function initMenuItems() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有菜单项的active类
            menuItems.forEach(i => i.classList.remove('active'));
            
            // 为当前点击的菜单项添加active类
            this.classList.add('active');
            
            // 更新面包屑
            updateBreadcrumb(this.querySelector('span').textContent);
        });
    });
}

// 更新面包屑
function updateBreadcrumb(text) {
    const breadcrumb = document.querySelector('.breadcrumb span');
    breadcrumb.textContent = text;
}

// 初始化创建机器人按钮
function initCreateRobotButton() {
    const createBtn = document.querySelector('.create-btn');
    
    if (createBtn) {
        createBtn.addEventListener('click', function() {
            // 显示创建机器人的模态框或跳转到创建页面
            alert('创建机器人功能即将上线，敬请期待！');
        });
    }
}

// 初始化添加机器人卡片
function initAddRobotCard() {
    const addRobotCard = document.querySelector('.add-robot-card');
    
    if (addRobotCard) {
        addRobotCard.addEventListener('click', function() {
            // 显示创建机器人的模态框或跳转到创建页面
            alert('创建机器人功能即将上线，敬请期待！');
        });
    }
}

// 初始化机器人卡片按钮
function initRobotCardButtons() {
    const robotButtons = document.querySelectorAll('.robot-btn');
    
    robotButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const buttonText = this.textContent.trim();
            const robotName = this.closest('.robot-card').querySelector('h3').textContent;
            
            if (buttonText === '管理') {
                alert(`正在打开 ${robotName} 的管理页面...`);
            } else if (buttonText === '对话') {
                alert(`正在打开与 ${robotName} 的对话页面...`);
            }
        });
    });
}

// 初始化刷新按钮
function initRefreshButton() {
    const refreshBtn = document.querySelector('.refresh-btn');
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            // 刷新页面数据
            alert('正在刷新数据...');
            location.reload();
        });
    }
}

// 添加响应式菜单切换功能
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
}

// 动态数据加载示例
function loadRobotData() {
    // 此处可以添加AJAX请求，从服务器获取机器人数据
    // 示例数据
    const robotData = [
        {
            name: '客服机器人',
            description: '专业客服，7x24小时在线',
            avatar: 'bot1.png',
            status: 'online',
            conversations: 3250,
            users: 125
        },
        {
            name: '销售助手',
            description: '智能销售，促进成交',
            avatar: 'bot2.png',
            status: 'online',
            conversations: 1420,
            users: 87
        },
        {
            name: '知识百科',
            description: '知识问答，回答各类问题',
            avatar: 'bot3.png',
            status: 'offline',
            conversations: 875,
            users: 56
        }
    ];
    
    // 更新界面
    updateRobotUI(robotData);
}

// 更新机器人UI
function updateRobotUI(robotData) {
    const robotGrid = document.querySelector('.robot-grid');
    const addRobotCard = document.querySelector('.add-robot-card');
    
    // 清空现有卡片（保留添加卡片）
    const existingCards = document.querySelectorAll('.robot-card:not(.add-robot-card)');
    existingCards.forEach(card => card.remove());
    
    // 添加新卡片
    robotData.forEach(robot => {
        const robotCard = createRobotCard(robot);
        robotGrid.insertBefore(robotCard, addRobotCard);
    });
    
    // 初始化新添加的卡片按钮
    initRobotCardButtons();
}

// 创建机器人卡片
function createRobotCard(robot) {
    const card = document.createElement('div');
    card.className = 'robot-card';
    
    card.innerHTML = `
        <div class="robot-header">
            <img src="${robot.avatar}" alt="${robot.name}" class="robot-avatar">
            <div class="robot-status ${robot.status}"></div>
        </div>
        <div class="robot-body">
            <h3>${robot.name}</h3>
            <p>${robot.description}</p>
            <div class="robot-stats">
                <div class="robot-stat">
                    <i class="fa fa-comment"></i>
                    <span>${robot.conversations}次对话</span>
                </div>
                <div class="robot-stat">
                    <i class="fa fa-users"></i>
                    <span>${robot.users}用户</span>
                </div>
            </div>
        </div>
        <div class="robot-footer">
            <button class="robot-btn">管理</button>
            <button class="robot-btn">对话</button>
        </div>
    `;
    
    return card;
} 