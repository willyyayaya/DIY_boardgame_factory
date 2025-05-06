from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
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

app = FastAPI(title="AI桌遊推薦工廠")

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

# 項目主入口
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8000) 