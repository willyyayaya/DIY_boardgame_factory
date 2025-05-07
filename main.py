from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
import json
import os
import openai
from pathlib import Path
from datetime import datetime

# 配置OpenAI (實際使用時需提供您的API密鑰)
# openai.api_key = "your-api-key-here"

# 創建必要的目錄
os.makedirs("templates", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("data/recommendations", exist_ok=True)
os.makedirs("data/preferences", exist_ok=True)
os.makedirs("data/designs", exist_ok=True)  # 添加設計存儲目錄

app = FastAPI(title="AI桌遊設計工廠")

# 靜態檔案和模板設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 數據模型
class BoardGamePreference(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player_count: str
    game_duration: str
    complexity: int = Field(ge=1, le=5)
    themes: List[str]
    mechanics: List[str]
    competitive_level: int = Field(ge=1, le=5)  # 1=合作, 5=高度對抗
    previous_games: Optional[List[str]] = None

class BoardGameRecommendation(BaseModel):
    id: str
    preference_id: str
    games: List[Dict[str, str]]  # 包含名稱、描述、連結等
    explanation: str
    created_at: str

# 新增: 桌遊設計模型
class BoardGameDesign(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    player_count: str
    duration: str
    complexity: int = Field(ge=1, le=5)
    themes: List[str]
    mechanics: List[str]
    atmosphere: str
    description: str
    theme_description: str
    components: List[str]
    objective: str
    setup: List[str]
    gameplay: str
    victory_condition: str
    strategy_tips: List[str]
    variants: List[str]
    created_at: str

# 新增: 桌遊設計需求模型
class BoardGameDesignRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    game_name: Optional[str] = None
    player_count: str
    game_duration: str
    complexity: int = Field(ge=1, le=5)
    themes: List[str]
    mechanics: List[str]
    atmosphere: str
    reference_games: Optional[str] = None
    special_requirements: Optional[str] = None
    design_template: str

# 保存用戶偏好和推薦
def save_preference(preference: BoardGamePreference):
    with open(f"data/preferences/{preference.id}.json", "w", encoding="utf-8") as f:
        f.write(preference.model_dump_json(indent=4))
    return preference.id

def save_recommendation(recommendation: BoardGameRecommendation):
    with open(f"data/recommendations/{recommendation.id}.json", "w", encoding="utf-8") as f:
        f.write(recommendation.model_dump_json(indent=4))
    return recommendation.id

def load_recommendation(recommendation_id: str) -> BoardGameRecommendation:
    try:
        with open(f"data/recommendations/{recommendation_id}.json", "r", encoding="utf-8") as f:
            return BoardGameRecommendation.model_validate_json(f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="推薦不存在")

# 新增: 保存桌遊設計需求
def save_design_request(design_request: BoardGameDesignRequest):
    with open(f"data/designs/request_{design_request.id}.json", "w", encoding="utf-8") as f:
        f.write(design_request.model_dump_json(indent=4))
    return design_request.id

# 新增: 保存桌遊設計
def save_game_design(design: BoardGameDesign):
    with open(f"data/designs/{design.id}.json", "w", encoding="utf-8") as f:
        f.write(design.model_dump_json(indent=4))
    return design.id

# 新增: 加載桌遊設計
def load_game_design(design_id: str) -> BoardGameDesign:
    try:
        with open(f"data/designs/{design_id}.json", "r", encoding="utf-8") as f:
            return BoardGameDesign.model_validate_json(f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="設計不存在")

# OpenAI API調用函數
def get_game_recommendations(preference: BoardGamePreference) -> Dict:
    try:
        # 構建提示詞
        prompt = f"""
        為一位玩家推薦5款適合的桌遊，並簡單解釋為什麼推薦。
        
        玩家喜好:
        - 玩家人數: {preference.player_count}
        - 遊戲時長: {preference.game_duration}
        - 複雜度: {preference.complexity}/5 (1為簡單，5為複雜)
        - 喜愛主題: {', '.join(preference.themes)}
        - 喜愛機制: {', '.join(preference.mechanics)}
        - 競爭程度偏好: {preference.competitive_level}/5 (1為合作型，5為高度競爭)
        - 曾經玩過的遊戲: {', '.join(preference.previous_games) if preference.previous_games else '無'}
        
        請以JSON格式回答，格式如下:
        {{
            "games": [
                {{
                    "name": "遊戲名稱",
                    "description": "一句話描述",
                    "reason": "為什麼這適合該玩家",
                    "player_count": "適合人數",
                    "duration": "遊戲時間",
                    "complexity": "複雜度(1-5)"
                }}
            ],
            "explanation": "整體推薦邏輯解釋"
        }}
        """
        
        # 使用模擬數據替代OpenAI API調用
        # 實際使用時，應該啟用以下代碼並使用有效的API密鑰
        
        """
        # 如果設置了API密鑰，使用OpenAI API
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        """
        
        # 模擬的回應數據 - 更豐富的推薦樣本
        # 根據不同的複雜度和偏好提供不同的推薦
        games_pool = {
            "簡單遊戲": [
                {
                    "name": "閃靈快手",
                    "description": "反應速度和觀察力的快節奏卡牌遊戲",
                    "reason": "簡單有趣，適合短時間遊戲，適合任何年齡層的玩家",
                    "player_count": "2-8人",
                    "duration": "15-20分鐘",
                    "complexity": "1/5"
                },
                {
                    "name": "矮人礦坑",
                    "description": "挖掘寶石的有趣卡牌遊戲",
                    "reason": "規則簡單易懂，但有策略深度，適合家庭遊戲",
                    "player_count": "3-7人",
                    "duration": "30分鐘",
                    "complexity": "1.5/5"
                },
                {
                    "name": "妙語說書人",
                    "description": "創意聯想和猜測的派對遊戲",
                    "reason": "非常適合大型聚會，激發創意思維",
                    "player_count": "3-12人",
                    "duration": "30-45分鐘",
                    "complexity": "1/5"
                }
            ],
            "中等複雜度": [
                {
                    "name": "卡卡頌",
                    "description": "放置拼圖建造中世紀景觀",
                    "reason": "簡單易學但有深度，適合各類玩家，策略性強",
                    "player_count": "2-5人",
                    "duration": "30-45分鐘",
                    "complexity": "2/5"
                },
                {
                    "name": "卡坦島",
                    "description": "經典資源管理與交易策略遊戲",
                    "reason": "平衡的資源收集和交易元素，適合家庭和朋友聚會",
                    "player_count": "3-4人",
                    "duration": "60-90分鐘",
                    "complexity": "2.5/5"
                },
                {
                    "name": "璀璨寶石",
                    "description": "收集寶石和發展的引擎構建遊戲",
                    "reason": "優雅的設計和精美的組件，適合喜歡引擎構建機制的玩家",
                    "player_count": "2-4人",
                    "duration": "30-45分鐘",
                    "complexity": "2/5"
                },
                {
                    "name": "瘟疫危機",
                    "description": "合作遊戲，玩家一起對抗全球瘟疫",
                    "reason": "適合喜愛合作機制的玩家，複雜度適中",
                    "player_count": "2-4人",
                    "duration": "45-60分鐘",
                    "complexity": "3/5"
                }
            ],
            "高複雜度": [
                {
                    "name": "拓荒者：帝國時代",
                    "description": "建立和發展你的帝國，積累資源和領土",
                    "reason": "結合了資源管理和領土擴張的策略元素，適合經驗豐富的玩家",
                    "player_count": "2-4人",
                    "duration": "60-90分鐘",
                    "complexity": "4/5"
                },
                {
                    "name": "凱旋門",
                    "description": "歐式重策略，建造古羅馬城市",
                    "reason": "深度策略和計劃性，適合喜歡思考型遊戲的玩家",
                    "player_count": "2-5人",
                    "duration": "60-90分鐘",
                    "complexity": "4/5"
                },
                {
                    "name": "星域奇航",
                    "description": "太空探索與戰略，建立星際帝國",
                    "reason": "複雜的經濟和戰爭系統，科幻主題吸引人",
                    "player_count": "3-6人",
                    "duration": "120-240分鐘",
                    "complexity": "4.5/5"
                },
                {
                    "name": "文明曙光",
                    "description": "打造你的文明，從石器時代到太空時代",
                    "reason": "深度的歷史主題和豐富的策略選擇",
                    "player_count": "2-4人",
                    "duration": "120-180分鐘",
                    "complexity": "4/5"
                }
            ]
        }
        
        # 收集相關主題的遊戲
        theme_based_games = {
            "奇幻": [
                {
                    "name": "魔法風雲會",
                    "description": "經典的奇幻收集卡牌對戰遊戲",
                    "reason": "豐富的奇幻世界觀和深度的策略性",
                    "player_count": "2人",
                    "duration": "20-40分鐘",
                    "complexity": "3.5/5"
                },
                {
                    "name": "小小世界",
                    "description": "奇幻種族征服世界的區域控制遊戲",
                    "reason": "有趣的奇幻種族組合和簡單明了的規則",
                    "player_count": "2-5人",
                    "duration": "40-80分鐘",
                    "complexity": "2.5/5"
                }
            ],
            "科幻": [
                {
                    "name": "克蘇魯疫症",
                    "description": "結合科幻與恐怖元素的合作遊戲",
                    "reason": "獨特的主題結合和緊張的遊戲體驗",
                    "player_count": "2-5人",
                    "duration": "120-180分鐘",
                    "complexity": "3.5/5"
                },
                {
                    "name": "背景輻射：廢土",
                    "description": "末日後世界的探索與生存",
                    "reason": "沉浸式的科幻末日世界和豐富的冒險",
                    "player_count": "1-4人",
                    "duration": "120-180分鐘",
                    "complexity": "3.5/5"
                }
            ],
            "歷史": [
                {
                    "name": "農家樂",
                    "description": "歷史背景的農場經營策略遊戲",
                    "reason": "經典歐式工人放置機制，有歷史主題",
                    "player_count": "1-4人",
                    "duration": "30-120分鐘",
                    "complexity": "3/5"
                },
                {
                    "name": "拜占庭將軍",
                    "description": "中世紀政治與貿易策略遊戲",
                    "reason": "深度的歷史背景和豐富的外交元素",
                    "player_count": "2-4人",
                    "duration": "60-120分鐘",
                    "complexity": "4/5"
                }
            ],
            "經濟": [
                {
                    "name": "鐵路之旅",
                    "description": "建造鐵路網絡連接城市",
                    "reason": "經典路線建設和集合套組遊戲",
                    "player_count": "2-5人",
                    "duration": "30-60分鐘",
                    "complexity": "2/5"
                },
                {
                    "name": "力量之塔",
                    "description": "能源市場競爭與發展",
                    "reason": "經濟主題的拍賣與資源管理",
                    "player_count": "2-6人",
                    "duration": "90-120分鐘",
                    "complexity": "3.5/5"
                }
            ]
        }
        
        # 根據偏好選擇遊戲
        selected_games = []
        
        # 1. 根據複雜度選擇
        complexity = preference.complexity
        if complexity <= 2:
            pool = games_pool["簡單遊戲"]
        elif complexity <= 3:
            pool = games_pool["中等複雜度"]
        else:
            pool = games_pool["高複雜度"]
            
        # 先添加1-2個複雜度匹配的遊戲
        selected_games.extend(pool[:2])
        
        # 2. 添加主題相關的遊戲
        for theme in preference.themes[:2]:  # 使用前兩個主題
            if theme in theme_based_games:
                for game in theme_based_games[theme][:1]:  # 每個主題最多添加1個
                    if len(selected_games) < 5:
                        selected_games.append(game)
        
        # 3. 如果還不夠5個，從其他池中添加
        if len(selected_games) < 5:
            all_games = []
            for category in games_pool:
                all_games.extend(games_pool[category])
            
            # 過濾掉已選的遊戲
            remaining_games = [g for g in all_games if g["name"] not in [sg["name"] for sg in selected_games]]
            
            # 添加剩餘的遊戲直到達到5個
            selected_games.extend(remaining_games[:5-len(selected_games)])
        
        # 確保只有5個遊戲
        selected_games = selected_games[:5]
        
        # 生成解釋
        themes_str = '、'.join(preference.themes[:2] if len(preference.themes) > 1 else preference.themes)
        mechanics_str = '、'.join(preference.mechanics[:2] if len(preference.mechanics) > 1 else preference.mechanics)
        
        explanation = f"根據您{preference.player_count}人的遊玩需求和{preference.game_duration}的時間限制，我選擇了一系列符合您對{themes_str}主題和{mechanics_str}機制偏好的遊戲。考慮到您{preference.complexity}/5的複雜度偏好，這些遊戲提供了各種層次的策略深度和挑戰。"
        
        result = {
            "games": selected_games,
            "explanation": explanation
        }
        
        return result
    except Exception as e:
        # 記錄錯誤並返回一個友好的信息
        print(f"Error generating recommendations: {str(e)}")
        return {"games": [], "explanation": "抱歉，處理您的請求時出錯。請稍後再試。"}

# 新增: 生成桌遊設計
def generate_game_design(design_request: BoardGameDesignRequest) -> Dict:
    try:
        # 構建提示詞
        prompt = f"""
        根據以下需求創建一個完整的桌遊設計方案。
        
        需求詳情:
        - 遊戲名稱: {design_request.game_name if design_request.game_name else "（請為我生成一個合適的名稱）"}
        - 玩家人數: {design_request.player_count}
        - 遊戲時長: {design_request.game_duration}
        - 複雜度: {design_request.complexity}/5 (1為簡單，5為複雜)
        - 主題: {', '.join(design_request.themes)}
        - 機制: {', '.join(design_request.mechanics)}
        - 預期氛圍: {design_request.atmosphere}
        - 參考遊戲: {design_request.reference_games if design_request.reference_games else "無"}
        - 特殊要求: {design_request.special_requirements if design_request.special_requirements else "無"}
        - 設計模板: {design_request.design_template}
        
        請以JSON格式回答，格式如下:
        {{
            "name": "遊戲名稱",
            "player_count": "適合人數",
            "duration": "遊戲時間",
            "complexity": "複雜度(1-5數字)",
            "themes": ["主題1", "主題2", ...],
            "mechanics": ["機制1", "機制2", ...],
            "atmosphere": "遊戲氛圍描述",
            "description": "遊戲整體設計概述",
            "theme_description": "主題和背景故事描述",
            "components": ["組件1", "組件2", ...],
            "objective": "遊戲目標描述",
            "setup": ["設置步驟1", "設置步驟2", ...],
            "gameplay": "遊戲流程的詳細HTML描述，含段落和列表",
            "victory_condition": "勝利條件描述",
            "strategy_tips": ["策略提示1", "策略提示2", ...],
            "variants": ["遊戲變體1", "遊戲變體2", ...]
        }}
        """
        
        # 使用模擬數據替代OpenAI API調用
        # 實際使用時，應該啟用以下代碼並使用有效的API密鑰
        
        """
        # 如果設置了API密鑰，使用OpenAI API
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.8
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        """
        
        # 模擬的回應數據 - 創建一個桌遊設計
        # 根據不同的模板和需求生成不同的設計
        
        # 決定合適的名稱
        game_name = design_request.game_name
        if not game_name:
            if "奇幻" in design_request.themes:
                game_name = "晶石傳說"
            elif "科幻" in design_request.themes:
                game_name = "星際殖民"
            elif "歷史" in design_request.themes:
                game_name = "文明曙光"
            elif "冒險" in design_request.themes:
                game_name = "探險隊長"
            else:
                game_name = "元素王國"
        
        # 基於模板創建遊戲設計
        templates = {
            "策略棋盤遊戲": {
                "description": "一款結合策略思考和資源管理的棋盤遊戲，玩家需要做出關鍵決策並規劃未來行動。",
                "components": [
                    f"主遊戲板 1 塊",
                    f"玩家板塊 {design_request.player_count.split('-')[1] if '-' in design_request.player_count else '4'} 塊",
                    "資源標記物 (木材、石頭、金幣等) 各 30 個",
                    "行動卡片 50 張",
                    "建築卡片 30 張",
                    "計分標記 1 套",
                    "規則手冊 1 本"
                ],
                "gameplay": """
                <p>遊戲進行多輪，每輪包含以下階段：</p>
                <ol>
                    <li><strong>收集資源階段：</strong>玩家根據自己的建築和板塊位置收集相應資源。</li>
                    <li><strong>行動階段：</strong>玩家輪流執行行動，每位玩家每輪可以執行2次行動。可用的行動包括：
                        <ul>
                            <li>使用資源建造建築</li>
                            <li>獲取新的行動卡片</li>
                            <li>移動自己的標記物</li>
                            <li>與其他玩家交易資源</li>
                        </ul>
                    </li>
                    <li><strong>回合結束階段：</strong>檢查是否達成任何成就或目標，更新計分板。</li>
                </ol>
                <p>遊戲持續進行直到觸發結束條件（通常是某玩家達到特定分數或建築數量）。</p>
                """
            },
            "卡牌遊戲": {
                "description": "一款豐富多變的卡牌遊戲，結合收集、組合和策略元素，讓玩家體驗緊張刺激的對抗。",
                "components": [
                    "角色卡 8 張",
                    "資源卡 60 張",
                    "行動卡 40 張",
                    "事件卡 20 張",
                    "玩家標記物 每位玩家 5 個",
                    "計分指示物 若干",
                    "規則手冊 1 本"
                ],
                "gameplay": """
                <p>遊戲進行多輪，每位玩家的回合包含三個主要步驟：</p>
                <ol>
                    <li><strong>抽牌階段：</strong>抽取2張卡片加入手牌。</li>
                    <li><strong>行動階段：</strong>玩家可以執行下列行動中的任意兩項：
                        <ul>
                            <li>打出一張資源卡</li>
                            <li>使用一張行動卡</li>
                            <li>激活自己場上的一個效果</li>
                            <li>與其他玩家交換一張手牌</li>
                        </ul>
                    </li>
                    <li><strong>結束階段：</strong>檢查手牌上限（通常為7張），必要時棄牌，然後檢查是否達成任何特殊條件。</li>
                </ol>
                <p>每當事件卡被抽出時，立即處理其效果，這會為遊戲帶來意外變化。</p>
                """
            },
            "派對遊戲": {
                "description": "一款充滿歡樂和互動的派對遊戲，適合社交場合，規則簡單但充滿樂趣。",
                "components": [
                    "提示卡 100 張",
                    "計時沙漏 1 個",
                    "計分板 1 個",
                    "標記物 每位玩家 1 個",
                    "特殊行動卡 20 張",
                    "規則手冊 1 本"
                ],
                "gameplay": """
                <p>遊戲以輪流為主，基本流程如下：</p>
                <ol>
                    <li><strong>準備階段：</strong>當前玩家抽取一張提示卡。</li>
                    <li><strong>表演階段：</strong>根據卡片指示，玩家可能需要：
                        <ul>
                            <li>描述特定詞語而不使用特定禁用詞</li>
                            <li>表演動作讓其他人猜測</li>
                            <li>在限時內畫出特定內容</li>
                            <li>與指定玩家協作完成挑戰</li>
                        </ul>
                    </li>
                    <li><strong>猜測階段：</strong>其他玩家嘗試猜出正確答案。</li>
                    <li><strong>計分階段：</strong>成功的表演和猜測都會獲得相應分數。</li>
                </ol>
                <p>特殊行動卡可以隨時使用，為遊戲增添變數和樂趣。</p>
                """
            },
            "角色扮演": {
                "description": "一款深度的角色扮演桌遊，玩家將進入豐富的世界觀，做出重要決策並推動故事發展。",
                "components": [
                    "角色卡 8 張",
                    "場景卡 30 張",
                    "事件卡 50 張",
                    "裝備卡 40 張",
                    "能力指示物 多種",
                    "地圖板塊 16 塊",
                    "角色立牌 8 個",
                    "骰子 4 個",
                    "規則手冊與故事指南 1 本"
                ],
                "gameplay": """
                <p>遊戲分為探索和事件兩種主要模式，按以下流程進行：</p>
                <ol>
                    <li><strong>探索模式：</strong>玩家輪流行動，每回合可以：
                        <ul>
                            <li>移動角色到新的地圖位置</li>
                            <li>與場景或NPC互動</li>
                            <li>使用或獲取裝備</li>
                            <li>執行角色特殊能力</li>
                        </ul>
                    </li>
                    <li><strong>事件模式：</strong>當觸發事件卡時，遊戲暫時進入事件解決階段：
                        <ul>
                            <li>閱讀事件描述</li>
                            <li>玩家做出選擇或執行挑戰</li>
                            <li>根據結果調整遊戲狀態</li>
                        </ul>
                    </li>
                    <li><strong>能力檢定：</strong>當需要判定成功與否時，玩家擲骰並與角色能力值相加，判定是否達到難度要求。</li>
                </ol>
                <p>遊戲可以跟隨主線故事發展，也可以自由探索支線任務和隱藏內容。</p>
                """
            },
            "資源管理": {
                "description": "一款精密的資源管理遊戲，玩家需要規劃資源分配、發展生產線並制定長期策略。",
                "components": [
                    "中央遊戲板 1 塊",
                    "玩家板塊 每位玩家 1 塊",
                    "資源立方體 5 種顏色各 30 個",
                    "建築卡/板塊 40 個",
                    "工人指示物 每位玩家 15 個",
                    "技術卡 30 張",
                    "市場卡 20 張",
                    "計分標記 每位玩家 1 個",
                    "輪數指示物 1 個",
                    "規則手冊 1 本"
                ],
                "gameplay": """
                <p>遊戲進行固定輪數（通常為6-8輪），每輪包含以下階段：</p>
                <ol>
                    <li><strong>收入階段：</strong>玩家根據自己的生產設施獲得資源。</li>
                    <li><strong>行動階段：</strong>玩家輪流放置工人執行行動，主要行動包括：
                        <ul>
                            <li>收集原材料</li>
                            <li>將原材料加工為更高級資源</li>
                            <li>建造新的建築或設施</li>
                            <li>研發新技術</li>
                            <li>在市場交易資源</li>
                            <li>執行特殊行動</li>
                        </ul>
                    </li>
                    <li><strong>維護階段：</strong>補充市場，更新公共區域，準備下一輪。</li>
                    <li><strong>結算階段：</strong>在最終輪結束後，根據建築、科技、資源和達成的目標計算最終得分。</li>
                </ol>
                <p>遊戲需要玩家平衡短期收益和長期發展，同時考慮稀缺資源的競爭。</p>
                """
            },
            "合作解謎": {
                "description": "一款刺激的合作解謎遊戲，玩家需要一起應對挑戰，解開謎題，在時間耗盡前達成目標。",
                "components": [
                    "遊戲場景卡 24 張",
                    "線索卡 60 張",
                    "挑戰卡 40 張",
                    "計時器 1 個",
                    "角色卡 6 張",
                    "特殊能力標記 每位玩家 3 個",
                    "解鎖工具 若干",
                    "謎題指示物 多種",
                    "規則手冊與謎題指南 1 本"
                ],
                "gameplay": """
                <p>遊戲是完全合作的，所有玩家一起工作解決謎題。基本流程如下：</p>
                <ol>
                    <li><strong>設置階段：</strong>根據選擇的劇本設置遊戲場景和初始線索。</li>
                    <li><strong>探索階段：</strong>玩家輪流或自由討論，執行以下行動：
                        <ul>
                            <li>檢查場景卡尋找線索</li>
                            <li>組合不同線索解開謎題</li>
                            <li>使用角色特殊能力協助團隊</li>
                            <li>在危機出現時做出決策</li>
                        </ul>
                    </li>
                    <li><strong>解謎階段：</strong>當發現足夠線索後，玩家可以嘗試解開主要謎題：
                        <ul>
                            <li>討論並提出可能的解答</li>
                            <li>使用解鎖工具驗證答案</li>
                            <li>根據反饋調整思路</li>
                        </ul>
                    </li>
                </ol>
                <p>遊戲通常有時間限制，玩家需要高效合作。成功解開所有謎題並完成最終目標即為勝利。</p>
                """
            }
        }
        
        # 獲取對應模板
        template = templates.get(design_request.design_template, templates["策略棋盤遊戲"])
        
        # 創建設計回應
        result = {
            "name": game_name,
            "player_count": design_request.player_count,
            "duration": design_request.game_duration,
            "complexity": design_request.complexity,
            "themes": design_request.themes,
            "mechanics": design_request.mechanics,
            "atmosphere": design_request.atmosphere,
            "description": template["description"],
            "theme_description": f"在{', '.join(design_request.themes[:2])}的世界背景下，玩家將體驗一場{design_request.atmosphere}的桌遊冒險。遊戲融合了{', '.join(design_request.mechanics[:3])}等核心機制，給玩家帶來獨特的遊戲體驗。",
            "components": template["components"],
            "objective": f"在遊戲中，玩家的目標是通過{design_request.mechanics[0] if design_request.mechanics else '策略思考'}和{design_request.mechanics[1] if len(design_request.mechanics) > 1 else '資源管理'}來獲得勝利點數。最終獲得最多點數的玩家將贏得遊戲。",
            "setup": [
                f"將主遊戲板放在桌子中央",
                f"每位玩家選擇一個顏色並拿取對應的玩家板塊和標記物",
                f"按照玩家人數調整遊戲元素和資源",
                f"每位玩家獲得起始資源和卡牌",
                f"隨機選擇一位玩家作為起始玩家"
            ],
            "gameplay": template["gameplay"],
            "victory_condition": f"遊戲結束後，玩家根據以下因素獲得分數：建築物、完成的目標、收集的資源和特殊成就。得分最高的玩家獲勝。",
            "strategy_tips": [
                f"前期專注於建立基礎資源生產",
                f"注意平衡短期收益和長期策略",
                f"留意其他玩家的動向並適時調整自己的計劃",
                f"合理利用特殊能力和卡牌效果",
                f"在遊戲後期注重獲取勝利點數的途徑"
            ],
            "variants": [
                f"二人變體：調整資源獲取和行動次數",
                f"團隊模式：玩家組成團隊共同對抗",
                f"快速模式：縮短遊戲時間的簡化規則",
                f"專家模式：增加額外的複雜規則和挑戰"
            ]
        }
        
        # 根據特殊要求進一步調整
        if design_request.special_requirements:
            result["description"] += f" {design_request.special_requirements}"
        
        return result
    except Exception as e:
        # 記錄錯誤並返回一個友好的信息
        print(f"Error generating game design: {str(e)}")
        return {
            "name": "設計生成錯誤",
            "description": "抱歉，處理您的請求時出錯。請稍後再試。", 
            "player_count": "未知", 
            "duration": "未知",
            "complexity": 1,
            "themes": [],
            "mechanics": [],
            "atmosphere": "未知",
            "theme_description": "",
            "components": ["無法生成組件"],
            "objective": "無法生成目標",
            "setup": ["無法生成設置步驟"],
            "gameplay": "<p>無法生成遊戲流程</p>",
            "victory_condition": "無法生成勝利條件",
            "strategy_tips": ["無法生成策略提示"],
            "variants": ["無法生成遊戲變體"]
        }

# 路由
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/preferences", response_class=HTMLResponse)
async def preference_form(request: Request):
    return templates.TemplateResponse("preferences.html", {"request": request})

@app.post("/submit-preferences")
async def submit_preferences(
    player_count: str = Form(...),
    game_duration: str = Form(...),
    complexity: int = Form(...),
    themes: List[str] = Form(...),
    mechanics: List[str] = Form(...),
    competitive_level: int = Form(...),
    previous_games: Optional[List[str]] = Form(None)
):
    # 創建偏好對象
    preference = BoardGamePreference(
        player_count=player_count,
        game_duration=game_duration,
        complexity=complexity,
        themes=themes,
        mechanics=mechanics,
        competitive_level=competitive_level,
        previous_games=previous_games if previous_games else []
    )
    
    # 保存偏好
    preference_id = save_preference(preference)
    
    # 獲取推薦
    result = get_game_recommendations(preference)
    
    # 創建並保存推薦
    recommendation = BoardGameRecommendation(
        id=str(uuid.uuid4()),
        preference_id=preference_id,
        games=result["games"],
        explanation=result["explanation"],
        created_at=str(datetime.now())
    )
    
    recommendation_id = save_recommendation(recommendation)
    
    # 重定向到結果頁面
    return RedirectResponse(url=f"/recommendations/{recommendation_id}", status_code=303)

@app.get("/recommendations/{recommendation_id}", response_class=HTMLResponse)
async def view_recommendation(request: Request, recommendation_id: str):
    recommendation = load_recommendation(recommendation_id)
    return templates.TemplateResponse("recommendation.html", {"request": request, "recommendation": recommendation})

# 新增: 設計問卷頁面路由
@app.get("/design-questionnaire", response_class=HTMLResponse)
async def design_questionnaire(request: Request):
    return templates.TemplateResponse("design-questionnaire.html", {"request": request})

# 新增: 提交設計需求路由
@app.post("/submit-design")
async def submit_design(
    game_name: Optional[str] = Form(None),
    player_count: str = Form(...),
    game_duration: str = Form(...),
    complexity: int = Form(...),
    themes: List[str] = Form(...),
    mechanics: List[str] = Form(...),
    atmosphere: str = Form(...),
    reference_games: Optional[str] = Form(None),
    special_requirements: Optional[str] = Form(None),
    design_template: str = Form(...)
):
    # 創建設計需求對象
    design_request = BoardGameDesignRequest(
        game_name=game_name,
        player_count=player_count,
        game_duration=game_duration,
        complexity=complexity,
        themes=themes,
        mechanics=mechanics,
        atmosphere=atmosphere,
        reference_games=reference_games,
        special_requirements=special_requirements,
        design_template=design_template
    )
    
    # 保存設計需求
    request_id = save_design_request(design_request)
    
    # 獲取設計
    result = generate_game_design(design_request)
    
    # 創建並保存設計
    design = BoardGameDesign(
        name=result["name"],
        player_count=result["player_count"],
        duration=result["duration"],
        complexity=result["complexity"],
        themes=result["themes"],
        mechanics=result["mechanics"],
        atmosphere=result["atmosphere"],
        description=result["description"],
        theme_description=result["theme_description"],
        components=result["components"],
        objective=result["objective"],
        setup=result["setup"],
        gameplay=result["gameplay"],
        victory_condition=result["victory_condition"],
        strategy_tips=result["strategy_tips"],
        variants=result["variants"],
        created_at=str(datetime.now())
    )
    
    design_id = save_game_design(design)
    
    # 重定向到結果頁面
    return RedirectResponse(url=f"/design-result/{design_id}", status_code=303)

# 新增: 設計結果頁面路由
@app.get("/design-result/{design_id}", response_class=HTMLResponse)
async def view_design(request: Request, design_id: str):
    design = load_game_design(design_id)
    return templates.TemplateResponse("design-result.html", {"request": request, "design": design})

# 新增: 下載設計PDF路由
@app.get("/download-design-pdf/{design_id}")
async def download_design_pdf(design_id: str):
    try:
        design = load_game_design(design_id)
        # 這裡應該實現PDF生成功能
        # 但需要額外的庫，例如ReportLab或WeasyPrint
        # 為簡化演示，只返回一個簡單的錯誤信息
        return {"message": "PDF下載功能正在開發中..."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成PDF時發生錯誤: {str(e)}")

# 新增: 設計修改頁面路由
@app.get("/refine-design/{design_id}", response_class=HTMLResponse)
async def refine_design(request: Request, design_id: str):
    design = load_game_design(design_id)
    return templates.TemplateResponse("design-questionnaire.html", {
        "request": request, 
        "design": design,
        "is_refine": True
    })

# 項目主入口
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8000) 