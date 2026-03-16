<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Prime AI | Author Command Center</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Orbitron:wght@700&display=swap');
        
        :root {
            --bg-dark: #090b11;
            --sidebar-bg: #11141d;
            --card-bg: #1a1f2e;
            --neon-blue: #00f2ff;
            --text-main: #e2e8f0;
            --glass: rgba(255, 255, 255, 0.03);
        }

        body {
            margin: 0;
            background: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* Sidebar Like Claude/ChatGPT */
        .sidebar {
            width: 260px;
            background: var(--sidebar-bg);
            border-right: 1px solid rgba(255,255,255,0.05);
            display: flex;
            flex-direction: column;
            padding: 20px;
        }

        .logo {
            font-family: 'Orbitron', sans-serif;
            color: var(--neon-blue);
            font-size: 1.2rem;
            margin-bottom: 40px;
            letter-spacing: 2px;
        }

        .nav-item {
            padding: 12px;
            margin: 4px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #94a3b8;
        }

        .nav-item:hover, .nav-item.active {
            background: var(--glass);
            color: var(--neon-blue);
        }

        /* Main Content Area */
        .main-content {
            flex: 1;
            overflow-y: auto;
            padding: 40px;
            background: radial-gradient(circle at top right, #101827, #090b11);
        }

        header {
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 1.8rem;
            margin: 0;
        }

        /* 17 Tools Grid Layout */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
        }

        .tool-card {
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .tool-card:hover {
            transform: translateY(-5px);
            border-color: var(--neon-blue);
            box-shadow: 0 10px 30px rgba(0, 242, 255, 0.1);
        }

        .tool-card i {
            font-size: 1.5rem;
            color: var(--neon-blue);
            margin-bottom: 15px;
        }

        .tool-card h3 {
            margin: 0;
            font-size: 1rem;
            font-weight: 600;
        }

        .tool-card p {
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 8px;
        }

        /* Status Badge */
        .badge {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 0.6rem;
            padding: 4px 8px;
            background: rgba(0, 242, 255, 0.1);
            color: var(--neon-blue);
            border-radius: 4px;
        }

    </style>
</head>
<body>

    <div class="sidebar">
        <div class="logo">NEXUS PRIME</div>
        <div class="nav-item active"><i class="fa-solid fa-house"></i> Dashboard</div>
        <div class="nav-item"><i class="fa-solid fa-pen-nib"></i> Writing Hub</div>
        <div class="nav-item"><i class="fa-solid fa-book-open"></i> KDP Suite</div>
        <div class="nav-item"><i class="fa-solid fa-photo-film"></i> Multimedia</div>
        <div class="nav-item"><i class="fa-solid fa-shield-halved"></i> Security Lab</div>
        <div style="margin-top: auto;" class="nav-item"><i class="fa-solid fa-gear"></i> Settings</div>
    </div>

    <div class="main-content">
        <header>
            <h1>Welcome back, Harun Rashid</h1>
            <p style="color: #64748b;">Commander, your 17 tactical tools are online.</p>
        </header>

        <div class="tools-grid">
            <div class="tool-card">
                <div class="badge">Point 1</div>
                <i class="fa-solid fa-feather"></i>
                <h3>Human Touch Tool</h3>
                <p>Add emotion to AI text.</p>
            </div>
            <div class="tool-card">
                <div class="badge">Point 2</div>
                <i class="fa-solid fa-magnifying-glass"></i>
                <h3>KDP Keywords</h3>
                <p>Rank your book on Top.</p>
            </div>
            <div class="tool-card">
                <div class="badge">Point 14</div>
                <i class="fa-solid fa-image"></i>
                <h3>Image Gen</h3>
                <p>Cyberpunk scene creator.</p>
            </div>
            <div class="tool-card">
                <div class="badge">Point 15</div>
                <i class="fa-solid fa-microphone-lines"></i>
                <h3>Realistic Voice</h3>
                <p>Text-to-Audiobooks.</p>
            </div>
            <div class="tool-card">
                <div class="badge">Point 16</div>
                <i class="fa-solid fa-calculator"></i>
                <h3>Cover Calc</h3>
                <p>Exact KDP dimensions.</p>
            </div>
            <div class="tool-card">
                <div class="badge">Point 8</div>
                <i class="fa-solid fa-robot"></i>
                <h3>AI Detector</h3>
                <p>Verify content integrity.</p>
            </div>
            </div>
    </div>

</body>
</html>
