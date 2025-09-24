# 🔑 API Keys Setup Guide

This guide will help you configure the necessary API keys to run RepoScope.

## 📋 Required APIs

### 🤖 LLM Provider (Required - Choose One)

You need **at least one** of these:

#### Option 1: OpenAI API
- **Cost**: ~$0.002 per 1K tokens (GPT-3.5-turbo)
- **Get API Key**: https://platform.openai.com/api-keys
- **Pros**: Most reliable, fastest
- **Cons**: More expensive

#### Option 2: OpenRouter API  
- **Cost**: Often 50-80% cheaper than OpenAI
- **Get API Key**: https://openrouter.ai/keys
- **Pros**: Cheaper, supports many models
- **Cons**: Slightly slower

### 🐙 GitHub API (Optional but Recommended)

- **Cost**: Free
- **Get Token**: https://github.com/settings/tokens
- **Permissions**: `public_repo` (read access)
- **Benefit**: Increases rate limit from 60 to 5000 requests/hour

## 🚀 Quick Setup

### Method 1: Interactive Setup (Recommended)

```bash
cd backend
python setup_api_keys.py
```

This script will guide you through the configuration process.

### Method 2: Manual Setup

1. Copy the example file:
```bash
cd backend
cp .env.example .env
```

2. Edit `.env` file and replace placeholder values:

```bash
# Choose one LLM provider
OPENAI_API_KEY=sk-your-actual-openai-key
# OR
OPENROUTER_API_KEY=sk-or-your-actual-openrouter-key
USE_OPENROUTER=true

# Optional but recommended
GITHUB_TOKEN=ghp_your-actual-github-token
```

## 🧪 Test Configuration

After setup, test your configuration:

```bash
cd backend
python test_api_connection.py
```

This will verify all API connections and test the full analysis workflow.

## 📊 Cost Estimation

### OpenAI Costs (GPT-3.5-turbo)
- **Input**: $0.0015 per 1K tokens
- **Output**: $0.002 per 1K tokens
- **Typical analysis**: ~2K tokens = ~$0.007 per repository

### OpenRouter Costs (varies by model)
- **GPT-3.5-turbo**: ~$0.001 per 1K tokens (50% cheaper)
- **Claude-3-haiku**: ~$0.0005 per 1K tokens (75% cheaper)
- **Llama models**: Often free or very cheap

### Example Monthly Costs
- **100 analyses/month**: $0.70 (OpenAI) or $0.35 (OpenRouter)
- **1000 analyses/month**: $7.00 (OpenAI) or $3.50 (OpenRouter)

## 🔒 Security Best Practices

### API Key Security
- ✅ Never commit API keys to git
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Use minimal required permissions

### GitHub Token Permissions
Only enable these permissions:
- `public_repo` - Access public repositories
- `read:user` - Read user profile (optional)

### Production Deployment
- Use secret management services (AWS Secrets Manager, etc.)
- Enable API key rotation
- Monitor usage and costs
- Set up billing alerts

## 🛠️ Troubleshooting

### Common Issues

#### "Invalid API key" Error
- Check key format: OpenAI starts with `sk-`, OpenRouter with `sk-or-`
- Verify key is active in your provider dashboard
- Check for extra spaces or characters

#### "Rate limit exceeded" Error
- Add GitHub token to increase limits
- Wait for rate limit reset (usually 1 hour)
- Consider using OpenRouter for higher limits

#### "Model not found" Error
- Check model name in `.env` file
- Verify model is available in your region
- Try different model (e.g., `gpt-3.5-turbo` instead of `gpt-4`)

### Getting Help

1. **Check logs**: Look at backend console output
2. **Test APIs**: Run `python test_api_connection.py`
3. **Verify config**: Run `python setup_api_keys.py` again
4. **Check documentation**: Provider-specific docs

## 📚 Provider-Specific Guides

### OpenAI Setup
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Add to `.env`: `OPENAI_API_KEY=sk-your-key`

### OpenRouter Setup
1. Go to https://openrouter.ai/keys
2. Sign up/login
3. Create new API key
4. Copy the key (starts with `sk-or-`)
5. Add to `.env`: `OPENROUTER_API_KEY=sk-or-your-key`
6. Set `USE_OPENROUTER=true`

### GitHub Token Setup
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select `public_repo` permission
4. Copy the token (starts with `ghp_`)
5. Add to `.env`: `GITHUB_TOKEN=ghp_your-token`

## 🎯 Next Steps

After configuring API keys:

1. **Test the setup**: `python test_api_connection.py`
2. **Start backend**: `python main.py`
3. **Start frontend**: `cd ../frontend && npm run dev`
4. **Open app**: http://localhost:3000
5. **Test analysis**: Try analyzing a public GitHub repository

## 💡 Tips for Cost Optimization

1. **Use OpenRouter**: Often 50-80% cheaper than OpenAI
2. **Choose efficient models**: GPT-3.5-turbo vs GPT-4
3. **Enable caching**: Set `ENABLE_CACHING=true`
4. **Limit token usage**: Set reasonable `MAX_TOKENS`
5. **Monitor usage**: Check provider dashboards regularly
