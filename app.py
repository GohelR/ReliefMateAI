<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReliefMate AI - Disaster Relief Assistant</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            overflow-x: hidden;
        }
        
        /* 3D Canvas Background */
        #canvas-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
        }
        
        /* Header */
        .header {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 20px 50px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            z-index: 1000;
            transition: all 0.3s ease;
        }
        
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 2rem;
            font-weight: bold;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { filter: drop-shadow(0 0 5px rgba(255, 107, 107, 0.5)); }
            to { filter: drop-shadow(0 0 20px rgba(78, 205, 196, 0.8)); }
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 30px;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            position: relative;
            transition: all 0.3s ease;
        }
        
        .nav-links a:hover {
            transform: translateY(-2px);
        }
        
        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            transition: width 0.3s ease;
        }
        
        .nav-links a:hover::after {
            width: 100%;
        }
        
        /* Hero Section */
        .hero {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
        }
        
        .hero-content {
            max-width: 800px;
            z-index: 10;
        }
        
        .hero-title {
            font-size: 4rem;
            margin-bottom: 20px;
            opacity: 0;
            transform: translateY(50px);
            animation: fadeInUp 1s ease 0.5s forwards;
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
            margin-bottom: 30px;
            opacity: 0;
            transform: translateY(50px);
            animation: fadeInUp 1s ease 0.8s forwards;
        }
        
        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 30px;
        }
        
        .cta-btn {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .cta-btn.primary {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
        }
        
        .cta-btn.secondary {
            background: transparent;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .cta-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        /* Sections */
        .section {
            padding: 100px 50px;
            position: relative;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-title {
            font-size: 3rem;
            text-align: center;
            margin-bottom: 60px;
            opacity: 0;
            transform: translateY(30px);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 60px;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            transform: translateY(50px);
            opacity: 0;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            display: block;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .feature-title {
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: #4ecdc4;
        }
        
        .feature-desc {
            line-height: 1.6;
            opacity: 0.9;
        }
        
        /* Chat Section */
        .chat-container {
            background: rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .chat-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .chat-box {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            min-height: 300px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .chat-input-container {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        
        .chat-input {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .chat-input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        .chat-input:focus {
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
        }
        
        .send-btn {
            padding: 15px 25px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border: none;
            border-radius: 25px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        /* Analytics Dashboard */
        .dashboard {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4ecdc4;
            margin-bottom: 10px;
        }
        
        .stat-label {
            opacity: 0.8;
        }
        
        /* Footer */
        .footer {
            background: rgba(0, 0, 0, 0.3);
            padding: 50px 0;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
            
            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .nav-links {
                display: none;
            }
            
            .section {
                padding: 50px 20px;
            }
        }
        
        /* Particle Effects */
        .particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: particleFloat 6s infinite linear;
        }
        
        @keyframes particleFloat {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) rotate(360deg);
                opacity: 0;
            }
        }
        
        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #4ecdc4;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- 3D Canvas Background -->
    <canvas id="canvas-bg"></canvas>
    
    <!-- Header -->
    <header class="header">
        <nav class="nav">
            <div class="logo">🌍 ReliefMate AI</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#chat">AI Assistant</a></li>
                <li><a href="#dashboard">Dashboard</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="particles"></div>
        <div class="hero-content">
            <h1 class="hero-title">🤝 Disaster Relief Assistant</h1>
            <p class="hero-subtitle">Powered by Advanced AI • Real-time Analytics • 24/7 Support</p>
            <div class="cta-buttons">
                <button class="cta-btn primary" onclick="scrollToSection('chat')">Start Chat</button>
                <button class="cta-btn secondary" onclick="scrollToSection('features')">Learn More</button>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section id="features" class="section">
        <div class="container">
            <h2 class="section-title">🌟 Powerful Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <h3 class="feature-title">AI Assistant</h3>
                    <p class="feature-desc">Get instant help with disaster relief queries, emergency protocols, and resource allocation using advanced AI technology.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📊</span>
                    <h3 class="feature-title">Real-time Reports</h3>
                    <p class="feature-desc">Track relief operations, monitor resource distribution, and get live updates on disaster response activities.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📈</span>
                    <h3 class="feature-title">Analytics Dashboard</h3>
                    <p class="feature-desc">Visualize data trends, analyze response effectiveness, and make data-driven decisions for better outcomes.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🚨</span>
                    <h3 class="feature-title">Emergency Alerts</h3>
                    <p class="feature-desc">Receive instant notifications about critical situations and coordinate rapid response efforts.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🌐</span>
                    <h3 class="feature-title">Multi-language Support</h3>
                    <p class="feature-desc">Communicate in multiple languages including Hindi, Gujarati, and English for better accessibility.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🔒</span>
                    <h3 class="feature-title">Secure & Reliable</h3>
                    <p class="feature-desc">Military-grade security with 99.9% uptime to ensure your critical operations never stop.</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- AI Chat Section -->
    <section id="chat" class="section">
        <div class="container">
            <div class="chat-container">
                <div class="chat-header">
                    <h2>💬 AI Assistant</h2>
                    <p>Ask me anything about disaster relief, emergency procedures, or resource management</p>
                </div>
                <div class="chat-box" id="chatBox">
                    <div style="text-align: center; opacity: 0.6; margin-top: 100px;">
                        <h3>🤖 ReliefMate AI Ready</h3>
                        <p>Type your question below to get started</p>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Ask about emergency procedures, resource allocation, or disaster response..." maxlength="500">
                    <button class="send-btn" onclick="sendMessage()">Send 🚀</button>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Dashboard Section -->
    <section id="dashboard" class="section">
        <div class="container">
            <h2 class="section-title">📈 Live Dashboard</h2>
            <div class="dashboard">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number" id="activeRequests">847</div>
                        <div class="stat-label">Active Requests</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="resolvedCases">12,459</div>
                        <div class="stat-label">Resolved Cases</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="totalUsers">25,678</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="responseTime">2.3s</div>
                        <div class="stat-label">Avg Response Time</div>
                    </div>
                </div>
                
                <div style="margin-top: 40px;">
                    <h3>🏥 Recent Relief Operations</h3>
                    <div style="margin-top: 20px;">
                        <div class="feature-card" style="margin-bottom: 15px;">
                            <h4 style="color: #ff6b6b;">🚨 Critical - Rajkot Flood Relief</h4>
                            <p>Status: Active • Needs: Food, Water, Medical Supplies • Team Dispatched</p>
                        </div>
                        <div class="feature-card" style="margin-bottom: 15px;">
                            <h4 style="color: #4ecdc4;">✅ Resolved - Ahmedabad Earthquake Response</h4>
                            <p>Status: Complete • Rescued: 45 people • Duration: 6 hours</p>
                        </div>
                        <div class="feature-card">
                            <h4 style="color: #ffd93d;">⚠️ Monitoring - Surat Cyclone Alert</h4>
                            <p>Status: Monitoring • Evacuation Ready • Emergency Teams on Standby</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <h3>🌍 ReliefMate AI</h3>
            <p>Saving lives through technology • Available 24/7 • Emergency: 112</p>
            <p style="margin-top: 20px; opacity: 0.6;">© 2025 ReliefMate AI. Powered by Gemini AI Technology.</p>
        </div>
    </footer>
    
    <script>
        // 3D Background Animation
        let scene, camera, renderer, particles;
        
        function init3D() {
            const canvas = document.getElementById('canvas-bg');
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            
            // Create particles
            const particleCount = 1000;
            const positions = new Float32Array(particleCount * 3);
            const colors = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 2000;
                positions[i + 1] = (Math.random() - 0.5) * 2000;
                positions[i + 2] = (Math.random() - 0.5) * 2000;
                
                colors[i] = Math.random();
                colors[i + 1] = Math.random();
                colors[i + 2] = Math.random();
            }
            
            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            
            const material = new THREE.PointsMaterial({ 
                size: 3, 
                vertexColors: true,
                transparent: true,
                opacity: 0.6
            });
            
            particles = new THREE.Points(geometry, material);
            scene.add(particles);
            
            camera.position.z = 500;
            animate3D();
        }
        
        function animate3D() {
            requestAnimationFrame(animate3D);
            particles.rotation.x += 0.001;
            particles.rotation.y += 0.002;
            renderer.render(scene, camera);
        }
        
        // Initialize 3D background
        init3D();
        
        // Resize handler
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        // Particle system for hero section
        function createParticles() {
            const particlesContainer = document.querySelector('.particles');
            
            setInterval(() => {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = particle.style.height = Math.random() * 10 + 5 + 'px';
                particle.style.animationDelay = Math.random() * 2 + 's';
                particlesContainer.appendChild(particle);
                
                setTimeout(() => {
                    particle.remove();
                }, 6000);
            }, 300);
        }
        
        createParticles();
        
        // Scroll animations
        function animateOnScroll() {
            const elements = document.querySelectorAll('.section-title, .feature-card');
            elements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const elementVisible = 150;
                
                if (elementTop < window.innerHeight - elementVisible) {
                    gsap.to(element, { opacity: 1, y: 0, duration: 1, ease: "power2.out" });
                }
            });
        }
        
        window.addEventListener('scroll', animateOnScroll);
        
        // Chat functionality
        let chatHistory = [];
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const chatBox = document.getElementById('chatBox');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage('user', message);
            input.value = '';
            
            // Show loading
            addMessage('ai', '<div class="loading"></div>', true);
            
            // Simulate AI response
            setTimeout(() => {
                removeLastMessage();
                const responses = [
                    "🚨 For immediate emergency assistance, call 112 (Police), 108 (Ambulance), or 101 (Fire). I can help you with resource allocation and disaster protocols.",
                    "📋 I can assist with evacuation procedures, emergency supplies checklist, and coordinating relief operations. What specific help do you need?",
                    "🏥 For medical emergencies during disasters, ensure ABC (Airway, Breathing, Circulation) first. Do you need specific medical protocol guidance?",
                    "🌊 Flood safety: Move to higher ground immediately, avoid walking/driving through flood water, and stay informed via official channels. Need specific flood response help?",
                    "🔥 Fire emergency: GET OUT, STAY OUT, CALL FOR HELP. Ensure everyone is out, close doors behind you, and meet at your family meeting spot."
                ];
                
                const response = responses[Math.floor(Math.random() * responses.length)];
                addMessage('ai', response);
            }, 2000);
        }
        
        function addMessage(sender, message, isLoading = false) {
            const chatBox = document.getElementById('chatBox');
            const messageDiv = document.createElement('div');
            messageDiv.style.cssText = `
                margin: 15px 0;
                padding: 15px;
                border-radius: 15px;
                background: ${sender === 'user' ? 'rgba(255, 107, 107, 0.2)' : 'rgba(78, 205, 196, 0.2)'};
                border-left: 4px solid ${sender === 'user' ? '#ff6b6b' : '#4ecdc4'};
                animation: slideIn 0.3s ease;
            `;
            
            messageDiv.innerHTML = `
                <div style="font-weight: bold; color: ${sender === 'user' ? '#ff6b6b' : '#4ecdc4'}; margin-bottom: 8px;">
                    ${sender === 'user' ? '👤 You' : '🤖 ReliefMate AI'}
                </div>
                <div>${message}</div>
            `;
            
            // Clear empty state if first message
            if (chatBox.children.length === 1 && chatBox.children[0].style.textAlign === 'center') {
                chatBox.innerHTML = '';
            }
            
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            if (isLoading) {
                messageDiv.classList.add('loading-message');
            }
        }
        
        function removeLastMessage() {
            const chatBox = document.getElementById('chatBox');
            const loadingMessage = chatBox.querySelector('.loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
        }
        
        // Enter key support for chat
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Smooth scrolling
        function scrollToSection(sectionId) {
            document.getElementById(sectionId).scrollIntoView({
                behavior: 'smooth'
            });
        }
        
        // Dynamic stats animation
        function animateStats() {
            const stats = [
                { id: 'activeRequests', target: 847 },
                { id: 'resolvedCases', target: 12459 },
                { id: 'totalUsers', target: 25678 }
            ];
            
            stats.forEach(stat => {
                const element = document.getElementById(stat.id);
                let current = 0;
                const increment = stat.target / 100;
                
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= stat.target) {
                        current = stat.target;
                        clearInterval(timer);
                    }
                    element.textContent = Math.floor(current).toLocaleString();
                }, 50);
            });
        }
        
        // Start stats animation when dashboard is visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && entry.target.id === 'dashboard') {
                    animateStats();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(document.getElementById('dashboard'));
        
        // Header scroll effect
        window.addEventListener('scroll', () => {
            const header = document.querySelector('.header');
            if (window.scrollY > 100) {
                header.style.background = 'rgba(0, 0, 0, 0.3)';
                header.style.backdropFilter = 'blur(30px)';
            } else {
                header.style.background = 'rgba(255, 255, 255, 0.1)';
                header.style.backdropFilter = 'blur(20px)';
            }
        });
        
        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateX(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
