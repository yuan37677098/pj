<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>灵境待办 | 优雅任务管理</title>
    <!-- Google Font & 现代字体方案 -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <!-- Font Awesome 6 (免费图标库) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, sans-serif;
            background: linear-gradient(145deg, #f0f4ff 0%, #e6edfc 100%);
            min-height: 100vh;
            padding: 2rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* 主卡片 - 玻璃质感 + 柔和阴影 */
        .todo-card {
            max-width: 700px;
            width: 100%;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(2px);
            border-radius: 2rem;
            box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25), 0 2px 5px rgba(0, 0, 0, 0.02);
            overflow: hidden;
            transition: all 0.2s ease;
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        /* 头部装饰区 */
        .hero {
            background: linear-gradient(135deg, #5b7cff, #7c5cff);
            padding: 2rem 2rem 1.8rem 2rem;
            color: white;
        }

        .hero-top {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-weight: 700;
            font-size: 1.9rem;
            letter-spacing: -0.5px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .hero h1 i {
            font-size: 1.8rem;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        }

        .date-badge {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(4px);
            padding: 0.4rem 1rem;
            border-radius: 40px;
            font-size: 0.85rem;
            font-weight: 500;
            letter-spacing: 0.3px;
        }

        .quote {
            font-size: 0.9rem;
            opacity: 0.9;
            font-weight: 400;
            margin-top: 0.5rem;
            border-left: 2px solid rgba(255,255,255,0.5);
            padding-left: 1rem;
        }

        /* 新增任务区域 */
        .add-task {
            padding: 1.8rem 2rem 0 2rem;
            background: transparent;
        }

        .input-group {
            display: flex;
            gap: 12px;
            background: white;
            border-radius: 80px;
            padding: 0.2rem 0.2rem 0.2rem 1.5rem;
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid #eef2ff;
            transition: all 0.2s;
        }

        .input-group:focus-within {
            box-shadow: 0 6px 18px rgba(92, 76, 255, 0.12);
            border-color: #a38eff;
        }

        .input-group input {
            flex: 1;
            border: none;
            padding: 1rem 0;
            font-size: 1rem;
            font-weight: 500;
            background: transparent;
            outline: none;
            color: #1f2937;
            font-family: 'Inter', monospace;
        }

        .input-group input::placeholder {
            color: #b9c2e0;
            font-weight: 400;
        }

        .input-group button {
            background: #5b7cff;
            border: none;
            color: white;
            font-weight: 600;
            padding: 0 1.6rem;
            border-radius: 60px;
            font-size: 0.95rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: 0.2s;
            font-family: inherit;
            letter-spacing: 0.3px;
        }

        .input-group button:hover {
            background: #4665e6;
            transform: scale(0.96);
            box-shadow: 0 5px 12px rgba(91, 124, 255, 0.3);
        }

        /* 工具栏 (过滤器 + 清除) */
        .toolbar {
            padding: 1.2rem 2rem 0.2rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .filters {
            display: flex;
            gap: 8px;
            background: #f3f6fe;
            padding: 5px;
            border-radius: 60px;
        }

        .filter-btn {
            border: none;
            background: transparent;
            padding: 0.5rem 1.2rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            transition: 0.2s;
            color: #4b5563;
        }

        .filter-btn.active {
            background: white;
            color: #5b7cff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .clear-completed {
            background: rgba(239, 68, 68, 0.08);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 40px;
            font-size: 0.8rem;
            font-weight: 500;
            color: #dc2626;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: 0.2s;
        }

        .clear-completed:hover {
            background: #fee2e2;
            color: #b91c1c;
        }

        /* 任务列表区域 */
        .task-container {
            padding: 0.5rem 2rem 1.5rem 2rem;
        }

        .task-list {
            list-style: none;
            margin: 0;
            max-height: 420px;
            overflow-y: auto;
            padding-right: 4px;
        }

        /* 自定义滚动条 */
        .task-list::-webkit-scrollbar {
            width: 5px;
        }
        .task-list::-webkit-scrollbar-track {
            background: #eef2ff;
            border-radius: 10px;
        }
        .task-list::-webkit-scrollbar-thumb {
            background: #c7d2fe;
            border-radius: 10px;
        }

        .task-item {
            background: white;
            margin-bottom: 12px;
            border-radius: 1.2rem;
            padding: 0.8rem 1rem 0.8rem 1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.2s;
            border: 1px solid #f0f2f8;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        }

        .task-item:hover {
            border-color: #dfe6ff;
            box-shadow: 0 8px 20px rgba(91, 124, 255, 0.08);
            transform: translateY(-1px);
        }

        .task-check {
            transform: scale(1.1);
            accent-color: #5b7cff;
            width: 1.2rem;
            height: 1.2rem;
            cursor: pointer;
        }

        .task-text {
            flex: 1;
            font-size: 0.98rem;
            font-weight: 500;
            color: #1f2937;
            word-break: break-word;
            padding-right: 8px;
            transition: 0.2s;
        }

        .task-text.completed {
            text-decoration: line-through;
            color: #9ca3af;
            font-weight: 400;
        }

        .task-actions {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .edit-btn, .delete-btn {
            background: transparent;
            border: none;
            font-size: 1rem;
            cursor: pointer;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: 0.2s;
            color: #6b7280;
        }

        .edit-btn:hover {
            background: #eef2ff;
            color: #5b7cff;
        }

        .delete-btn:hover {
            background: #fee2e2;
            color: #ef4444;
        }

        /* 空状态 */
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #9aa9c1;
        }

        .empty-state i {
            font-size: 3rem;
            margin-bottom: 0.8rem;
            opacity: 0.5;
        }

        .stats {
            margin-top: 1rem;
            font-size: 0.75rem;
            color: #5e6f8d;
            text-align: center;
            border-top: 1px solid #eef2ff;
            padding-top: 1rem;
            font-weight: 500;
        }

        footer {
            padding: 1rem 2rem 1.6rem;
            text-align: center;
            font-size: 0.7rem;
            color: #8d9ac2;
            background: rgba(255,255,240,0.2);
        }

        @media (max-width: 550px) {
            body {
                padding: 1rem;
            }
            .hero h1 {
                font-size: 1.5rem;
            }
            .input-group button {
                padding: 0 1rem;
            }
            .toolbar {
                flex-direction: column;
                align-items: stretch;
            }
            .filters {
                justify-content: center;
            }
            .task-item {
                flex-wrap: wrap;
            }
            .task-actions {
                margin-left: auto;
            }
        }
    </style>
</head>
<body>
<div class="todo-card">
    <div class="hero">
        <div class="hero-top">
            <h1>
                <i class="fas fa-check-circle"></i> 
                灵境待办
            </h1>
            <div class="date-badge" id="currentDate"></div>
        </div>
        <div class="quote">
            <i class="fas fa-feather-alt" style="margin-right: 6px;"></i> 清晰思绪 · 轻盈完成
        </div>
    </div>

    <div class="add-task">
        <div class="input-group">
            <input type="text" id="taskInput" placeholder="写一个优雅的任务..." autocomplete="off">
            <button id="addTaskBtn">
                <i class="fas fa-plus"></i> 添加
            </button>
        </div>
    </div>

    <div class="toolbar">
        <div class="filters">
            <button class="filter-btn active" data-filter="all">全部</button>
            <button class="filter-btn" data-filter="active">未完成</button>
            <button class="filter-btn" data-filter="completed">已完成</button>
        </div>
        <button class="clear-completed" id="clearCompletedBtn">
            <i class="fas fa-trash-alt"></i> 清除已完成
        </button>
    </div>

    <div class="task-container">
        <ul class="task-list" id="taskList"></ul>
        <div class="stats" id="statsInfo">
            <!-- 动态统计 -->
        </div>
    </div>
    <footer>
        <i class="fas fa-save"></i> 自动保存 · 灵感不丢失
    </footer>
</div>

<script>
    // ---------- 带领小白一步一步构建待办应用 ----------
    // 所有任务存储
    let tasks = [];
    // 当前过滤模式: 'all', 'active', 'completed'
    let currentFilter = 'all';

    // DOM 元素
    const taskListEl = document.getElementById('taskList');
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addTaskBtn');
    const clearCompletedBtn = document.getElementById('clearCompletedBtn');
    const statsInfo = document.getElementById('statsInfo');
    const filterBtns = document.querySelectorAll('.filter-btn');

    // 辅助函数：获取当前日期 (美观显示)
    function updateDate() {
        const now = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
        const dateStr = now.toLocaleDateString('zh-CN', options);
        document.getElementById('currentDate').innerHTML = `<i class="far fa-calendar-alt"></i> ${dateStr}`;
    }

    // 保存任务到 localStorage
    function saveTasksToLocal() {
        localStorage.setItem('elegant_todo_app', JSON.stringify(tasks));
    }

    // 加载初始数据 (若没有则使用示例任务)
    function loadInitialTasks() {
        const stored = localStorage.getItem('elegant_todo_app');
        if (stored) {
            tasks = JSON.parse(stored);
        } else {
            // 优雅的示例任务，展示功能
            tasks = [
                { id: Date.now() + 1, text: '🌟 点击复选框标记完成', completed: false },
                { id: Date.now() + 2, text: '✏️ 点击编辑按钮修改任务内容', completed: false },
                { id: Date.now() + 3, text: '🗑️ 试试删除任务 (有确认提示)', completed: true },
                { id: Date.now() + 4, text: '🎨 支持“清除已完成”一键整理', completed: false }
            ];
            saveTasksToLocal();
        }
    }

    // 更新未完成任务数量 & 统计展示
    function updateStats() {
        const total = tasks.length;
        const activeCount = tasks.filter(t => !t.completed).length;
        const completedCount = total - activeCount;
        let message = '';
        if (total === 0) {
            message = '✨ 暂无任务，添加一条新任务吧';
        } else {
            message = `📋 总计 ${total} 项  · 待完成 ${activeCount} 项  · 已完成 ${completedCount} 项`;
        }
        statsInfo.innerHTML = `<i class="fas fa-chart-simple"></i> ${message}`;
        
        // 控制清除已完成按钮的视觉提示 (如果无已完成任务，样式变淡，但仍然可点，逻辑会提示)
        if (completedCount === 0) {
            clearCompletedBtn.style.opacity = '0.6';
        } else {
            clearCompletedBtn.style.opacity = '1';
        }
    }

    // 核心渲染函数: 根据 currentFilter 和 tasks 重新绘制列表
    function renderTasks() {
        // 1. 过滤任务
        let filteredTasks = [];
        if (currentFilter === 'all') {
            filteredTasks = [...tasks];
        } else if (currentFilter === 'active') {
            filteredTasks = tasks.filter(task => !task.completed);
        } else if (currentFilter === 'completed') {
            filteredTasks = tasks.filter(task => task.completed);
        }

        // 2. 清空列表容器
        taskListEl.innerHTML = '';

        // 3. 若没有任务展示空状态
        if (filteredTasks.length === 0) {
            const emptyDiv = document.createElement('li');
            emptyDiv.className = 'empty-state';
            emptyDiv.innerHTML = `
                <i class="far fa-smile-wink"></i>
                <p>这里空空如也～<br>${currentFilter === 'all' ? '添加新任务开启高效一天' : currentFilter === 'active' ? '所有任务都完成了！太棒了 🎉' : '暂无已完成的任务'}</p>
            `;
            taskListEl.appendChild(emptyDiv);
            updateStats();
            return;
        }

        // 4. 循环生成每个任务 DOM (使用 document fragment 提升性能)
        const fragment = document.createDocumentFragment();
        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item';
            // 把任务 id 存储在 li 上，方便事件委托获取
            li.dataset.id = task.id;

            // 复选框
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'task-check';
            checkbox.checked = task.completed;
            // 存储 id 以防万一
            checkbox.dataset.id = task.id;

            // 任务文本 span
            const taskSpan = document.createElement('span');
            taskSpan.className = 'task-text';
            if (task.completed) taskSpan.classList.add('completed');
            taskSpan.textContent = task.text;  // 自动转义，防止XSS

            // 操作按钮组
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'task-actions';

            const editBtn = document.createElement('button');
            editBtn.className = 'edit-btn';
            editBtn.innerHTML = '<i class="fas fa-pen"></i>';
            editBtn.title = '编辑任务';

            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-btn';
            deleteBtn.innerHTML = '<i class="fas fa-trash-can"></i>';
            deleteBtn.title = '删除任务';

            actionsDiv.appendChild(editBtn);
            actionsDiv.appendChild(deleteBtn);

            li.appendChild(checkbox);
            li.appendChild(taskSpan);
            li.appendChild(actionsDiv);
            fragment.appendChild(li);
        });
        taskListEl.appendChild(fragment);
        
        // 更新统计数字
        updateStats();
        // 更新过滤器按钮高亮样式
        updateFilterActiveStyle();
    }

    // 高亮当前激活的过滤按钮
    function updateFilterActiveStyle() {
        filterBtns.forEach(btn => {
            const filterValue = btn.getAttribute('data-filter');
            if (filterValue === currentFilter) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // 刷新整个UI并保存到本地 (修改数据后必须调用)
    function refreshUI() {
        saveTasksToLocal();
        renderTasks();
    }

    // ---------- 核心业务逻辑 ----------
    // 添加新任务
    function addNewTask() {
        const rawText = taskInput.value.trim();
        if (rawText === '') {
            // 简单提示，不暴力弹窗，用自然反馈（可模仿占位提示）
            taskInput.placeholder = '请先输入一些内容～';
            taskInput.style.border = '1px solid #ffc6c6';
            setTimeout(() => {
                taskInput.placeholder = '写一个优雅的任务...';
                taskInput.style.border = '';
            }, 1200);
            return;
        }
        // 创建任务对象
        const newTask = {
            id: Date.now(),
            text: rawText,
            completed: false,
        };
        tasks.push(newTask);
        // 添加任务后，将过滤器重置为「全部」，这样用户能立即看到新任务（符合直觉）
        currentFilter = 'all';
        // 清空输入框
        taskInput.value = '';
        // 刷新界面
        refreshUI();
        // 让输入框重新获得焦点
        taskInput.focus();
    }

    // 删除任务 (带确认)
    function deleteTaskById(taskId) {
        const taskToDelete = tasks.find(t => t.id == taskId);
        if (!taskToDelete) return;
        const confirmDel = confirm(`确定要删除任务「${taskToDelete.text}」吗？`);
        if (confirmDel) {
            tasks = tasks.filter(t => t.id != taskId);
            refreshUI();
        }
    }

    // 编辑任务文本 (弹窗简洁)
    function editTaskById(taskId) {
        const task = tasks.find(t => t.id == taskId);
        if (!task) return;
        const newText = prompt('编辑你的任务', task.text);
        if (newText !== null && newText.trim() !== '') {
            task.text = newText.trim();
            refreshUI();
        } else if (newText !== null && newText.trim() === '') {
            alert('任务内容不能为空，未做修改');
        }
    }

    // 切换任务的完成状态
    function toggleTaskComplete(taskId, isChecked) {
        const task = tasks.find(t => t.id == taskId);
        if (task) {
            task.completed = isChecked;
            refreshUI();
        }
    }

    // 清除所有已完成的任务 (带确认)
    function clearCompletedTasks() {
        const completedTasks = tasks.filter(t => t.completed);
        if (completedTasks.length === 0) {
            alert('🎉 当前没有已完成的任务，无需清理');
            return;
        }
        const confirmClear = confirm(`确定要清除全部 ${completedTasks.length} 项已完成的任务吗？`);
        if (confirmClear) {
            tasks = tasks.filter(t => !t.completed);
            // 如果当前过滤器是 'completed' 并且清除后没有已完成任务了，可以切换至全部避免空白尴尬
            if (currentFilter === 'completed' && tasks.filter(t => t.completed).length === 0) {
                currentFilter = 'all';
            }
            refreshUI();
        }
    }

    // 切换过滤器
    function setFilter(filter) {
        if (filter === 'all' || filter === 'active' || filter === 'completed') {
            currentFilter = filter;
            renderTasks();  // 只需重新渲染，不修改数据
        }
    }

    // ---------- 事件委托 (高效监听动态生成的按钮及复选框) ----------
    function setupEventDelegation() {
        // 任务列表的点击事件 (用于处理编辑、删除以及复选框的点击——注意复选框用change更佳)
        taskListEl.addEventListener('click', (e) => {
            // 编辑按钮
            const editButton = e.target.closest('.edit-btn');
            if (editButton) {
                const li = editButton.closest('.task-item');
                if (li && li.dataset.id) {
                    editTaskById(Number(li.dataset.id));
                }
                e.stopPropagation();
                return;
            }

            // 删除按钮
            const deleteButton = e.target.closest('.delete-btn');
            if (deleteButton) {
                const li = deleteButton.closest('.task-item');
                if (li && li.dataset.id) {
                    deleteTaskById(Number(li.dataset.id));
                }
                e.stopPropagation();
                return;
            }
        });

        // 处理复选框状态变更 (change 事件)
        taskListEl.addEventListener('change', (e) => {
            const checkbox = e.target.closest('.task-check');
            if (checkbox) {
                const li = checkbox.closest('.task-item');
                if (li && li.dataset.id) {
                    toggleTaskComplete(Number(li.dataset.id), checkbox.checked);
                }
                e.stopPropagation();
            }
        });
    }

    // 过滤按钮监听
    function bindFilterButtons() {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const filterValue = btn.getAttribute('data-filter');
                setFilter(filterValue);
            });
        });
    }

    // 添加任务监听 (按钮 & 回车)
    function bindAddEvent() {
        addBtn.addEventListener('click', () => {
            addNewTask();
        });
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addNewTask();
            }
        });
    }

    // 清除已完成按钮监听
    function bindClearCompleted() {
        clearCompletedBtn.addEventListener('click', () => {
            clearCompletedTasks();
        });
    }

    // ---------- 初始化整个应用 ----------
    function init() {
        updateDate();           // 显示动态日期
        loadInitialTasks();    // 从本地加载或默认数据
        setupEventDelegation();// 全局事件委托
        bindFilterButtons();   // 过滤器点击
        bindAddEvent();        // 添加任务
        bindClearCompleted();  // 清除已完成
        renderTasks();         // 初次渲染
        // 定时刷新日期（跨日效果）
        setInterval(() => updateDate(), 60000);
    }

    // 启动应用
    init();
</script>
</body>
</html>
