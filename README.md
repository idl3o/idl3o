
[home](https://idl3o.github.io/gh-pages)

# Token-Based Creator Economy Streaming Service

This application demonstrates a streaming service with token-based creator economy, featuring AI-powered content generation, token rewards for creators and consumers, advanced health monitoring with RMB/GBT exchange, and Excelsior premium features.

## Key Features

### Health Service with RMB/GBT Exchange
- Comprehensive system monitoring with mathematical health metrics
- RMB/GBT currency exchange integration for global transactions
- Excelsior premium health features for enhanced reliability
- Token-based incentives for system monitoring and maintenance

#### Health Service Endpoints

```
GET /health
Response: Comprehensive health status with metrics

GET /api/health/metrics
Response: Detailed system metrics and service dependencies

GET /api/exchange/rates
Response: Current RMB/GBT exchange rates

POST /api/exchange/convert
{
  "amount": 100,
  "targetCurrency": "RMB"
}
Response: Converted token amount with exchange data

POST /api/excelsior/subscribe
{
  "userId": "creator1",
  "features": ["predictiveScaling", "redundantBackups", "crossChainBridge"]
}
Response: Excelsior subscription details
```

### Excelsior Premium Features
| Feature | Description | Token Cost |
|---------|-------------|------------|
| predictiveScaling | Predictive resource analytics | 0.5 tokens/day |
| redundantBackups | Enhanced backup monitoring | 0.2 tokens/day |
| priorityRecovery | Fast system recovery | 0.8 tokens/day |
| crossChainBridge | Multi-chain token bridge | 1.0 tokens/day |
| aiHealthOptimization | AI-driven system optimization | 1.5 tokens/day |

### Token Economics
- Cobb-Douglas production function for reward distribution: R = C^α * V^β
- Exponential emission decay function: E(t) = E₀ × λ^t
- Token-gated service access with mathematical scaling

### Java Debug Commands with Token Integration

The platform provides token-gated Java debugging capabilities. Higher token balances unlock more advanced debugging features.

#### Java Debug CLI Usage

```bash
# Start Java application with debugging enabled (consumes tokens)
./scripts/java-debug.sh start [class-or-jar] --token-level creator

# Attach debugger to running Java process
./scripts/java-debug.sh attach [pid] [user-id]

# Check debug session status and token consumption
./scripts/java-debug.sh status [user-id]
```

#### Token-Based Debug Access Levels

| Level | Min Balance | Capabilities | Token Cost |
|-------|-------------|--------------|------------|
| Consumer | 5 | Basic connection | 0.1 tokens/min |
| Creator | 20 | Variables, Hotswap | 0.1 tokens/min |
| Admin | 50 | Memory analysis, Threads | 0.1 tokens/min |

### AI-Powered Content Generation
- Natural language processing using GPT models
- Mathematical personality modeling: P = (empathy, creativity, precision)
- Memory system with recency bias function: f(t) = exp(-λt)
- Response generation bounded by O(log n) complexity

### Content Valuation & Rewards
- Content filtering using sigmoid threshold: σ(x) = 1/(1+e^(-x))
- Rate limiting with token bucket algorithm B(t) = min(B(t-1) + r, B_max)
- Staking mechanism with continuous compounding: A = Pe^(rt)
- Temperature modulation via linear combination T = λ₁v₁ + λ₂v₂ + λ₃v₃

## Voice Assistant Integration (AMA)

The platform includes an "Ask Me Anything" (AMA) voice assistant that integrates with popular voice platforms and rewards users with tokens for voice interactions.

### Supported Voice Platforms

- **Amazon Alexa**: Use the Token Economy skill to ask questions and earn tokens
- **Apple Siri**: Configure Siri Shortcuts to interact with the token economy
- **Home Assistant**: Integrate with your home automation system

### Voice AMA Features

- Token rewards for voice questions using mathematical reward model
- Conversation context awareness for multi-turn interactions
- Integration with the core token economy system
- Voice-based token balance inquiries

### API Endpoints

```
# Alexa Skill Endpoint
POST /api/voice/alexa

# Siri Shortcut Endpoint
POST /api/voice/siri
{
  "question": "How does token economy work?",
  "userId": "user123",
  "shortcutId": "token_ama"
}

# Home Assistant Integration
POST /api/voice/home-assistant
{
  "question": "What is my token balance?",
  "userId": "user123",
  "entityId": "token_assistant"
}

# Voice Platform Configuration
GET /api/voice/config?platform=alexa|siri|home-assistant

# Voice Interaction Statistics
GET /api/voice/stats
```

### Token Rewards for Voice

Voice interactions earn tokens based on:
- Question complexity (length and context)
- User frequency (regular users earn bonus rewards)
- Platform-specific factors

| Interaction Type | Base Reward | Complexity Bonus | Frequency Bonus |
|------------------|-------------|-----------------|-----------------|
| Voice Question   | 0.05 tokens | Up to 120%      | Up to 10%       |

## API Usage

### Chat Endpoint
```POST /api/chat
{
  "message": "Your message here"
}
```

Response:
```json
{
  "message": "AI response",
  "metadata": {
    "filtered": boolean,
    "rateLimits": {
      "remaining": number,
      "limit": number
    },
    "tokenRewards": {
      "earned": number,
      "cached": boolean
    }
  }
}
```

## Google Cloud Integration

The service automatically handles Google Cloud CLI availability, with graceful fallback to local mode when the CLI is unavailable. This ensures token operations continue even when cloud connectivity is limited.

## Development

### Installing Dependencies
```bash
npm ci  # Use this to install exact versions from package-lock.json
```

## Deployment
1. Provide OpenAI API key: `export OPENAI_API_KEY=your_key_here`
2. Select 'Deploy to Cloud Run' from Cloud Code
3. Deploy with token economics parameters: 
   ```
   TOKEN_EMISSION_RATE=1000 CREATOR_RATIO=0.7 CONSUMER_RATIO=0.2 EXCHANGE_ENABLED=true EXCELSIOR_ENABLED=true node app.js
   ```
