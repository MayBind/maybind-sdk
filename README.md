<div style="width: 100vw; margin-left: calc(-50vw + 50%); margin-right: calc(-50vw + 50%); padding: 0;">
  <img src="assets/maybind-logo.jpg" alt="MayBind Logo" style="width: 100%; display: block; margin: 0; padding: 0;">
</div>

<div align="center" style="margin-top: 20px;">
  
  [![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
  [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
  [![Build](https://img.shields.io/badge/build-passing-brightgreen)](sdk/)
  [![API Docs](https://img.shields.io/badge/docs-Swagger-blue?logo=swagger)](https://maybind.github.io/maybind-sdk/swagger/)
  
</div>

> **Official SDK for MayBind Digital Twin Platform**  
> Build and interact with AI digital twins through our comprehensive API

[MayBind](https://maybind.com) empowers users to create AI twins from conversation history and enables developers to build and monetize twin services through our marketplace.

## Core Features

**✅ Available Now**
- **⚡ Rapid Setup** - Get started with setup_quick.py in under 5 minutes
- **🤖 AI Agent Chat** - Conversational agents that simulate user behaviors (powered by Google Gemini)
- **Production-Ready** - API key authentication, usage tracking, enterprise reliability
- **Agent Discovery** - Automatic detection and selection of available AI agents
- **Python SDK** - Complete SDK with examples, tests, and documentation

**🚧 Coming Soon**  
- **JavaScript/Node.js SDK** - Full-featured web and Node.js support
- **Go SDK** - High-performance SDK for Go developers
- **Custom Agent Training** - Train agents to simulate specific user behaviors
- **Marketplace Integration** - Publish and monetize your agent-based services

## Project Structure

```
maybind-sdk/
├── 📄 README.md               # Overview and quick start
├── 📁 openapi/               # API specifications  
├── 📁 scripts/               # Development tools
└── 📁 sdk/                   # Multi-language SDKs
    └── python/               # 🐍 Python SDK
        ├── 📄 README.md      # Complete Python guide
        ├── 📄 setup_quick.py  # Interactive setup
        ├── 📁 examples/      # Working examples
        └── 📁 tests/         # Test suite
```

## Getting Started

**Ready to build with AI twins?** [Get your API key](https://maybind.com/auth?type=developer) and jump to [Quick Start](#-quick-start) ⬇️

## Usage Preview

```python
# Chat with an AI twin in 3 lines
api = DefaultApi()  # Auto-configured with .env
response = api.chat_chat_post(ChatRequest(twin_id="01", messages=[...]))
print(response.messages[-1]['text'])  # Twin's response
```

## Authentication

Get your API key from [MayBind Developer Dashboard](https://maybind.com/auth?type=developer):

```bash
# Set your API key
export MAYBIND_API_KEY="your_api_key_here"
```

## Installation


### Quick Start

#### Python SDK

```bash
# 1. Clone and setup
git clone https://github.com/MayBind/maybind-sdk.git
cd maybind-sdk/sdk/python

# 2. Run quick setup (interactive configuration)
python setup_quick.py

# 3. Test with examples
python examples/example_chat.py
```

The `setup_quick.py` script will:
- ✅ Install dependencies automatically
- ✅ Create `.env` configuration file
- ✅ Verify your API key with usage stats
- ✅ Test the connection

📖 **Complete Python guide**: [`sdk/python/README.md`](sdk/python/README.md)

## SDK Documentation

| Language | Status | Documentation | Examples |
|----------|--------|---------------|----------|
| **Python** | ✅ Ready | [`sdk/python/README.md`](sdk/python/README.md) | [`examples/`](sdk/python/examples/) |
| **JavaScript** | 🚧 Coming Soon | - | - |
| **Go** | 🚧 Coming Soon | - | - |

📘 **Full API reference (Swagger)**: [https://maybind.github.io/maybind-sdk/swagger/](https://maybind.github.io/maybind-sdk/swagger/)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** - Click "Fork" on GitHub to create your copy
2. **Create feature branch** - `git checkout -b feature/your-feature-name`  
3. **Commit changes** - `git commit -m 'Add: your feature description'`
4. **Push branch** - `git push origin feature/your-feature-name`
5. **Open Pull Request** - Go to GitHub and click "Compare & pull request"

**Branch examples**: `feature/javascript-sdk`, `bugfix/api-timeout`, `docs/quickstart-guide`

### Generate SDK
```bash
./scripts/generate_sdk.sh     # Unix/Linux/macOS
scripts\generate_sdk.bat      # Windows
```

### API Specification
OpenAPI spec: [`openapi/maybind-api.yaml`](openapi/maybind-api.yaml)

## 📋 Requirements

- **Python**: 3.9+
- **API Key**: From [MayBind Developer Dashboard](https://maybind.com)

## 📈 Roadmap

- **v1.0** ✅ Python SDK with chat and twin management
- **v1.1** 🚧 JavaScript/Node.js SDK  
- **v1.2** 🚧 Go SDK
- **v2.0** 🚧 Advanced twin customization features

## 🆘 Support

- **📖 Documentation**: Check SDK-specific README files
- **🐛 Issues**: [GitHub Issues](https://github.com/MayBind/maybind-sdk/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/MayBind/maybind-sdk/discussions)
- **🌐 Contact**: Visit our dedicated support section at [https://maybind.com](https://maybind.com)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🌟 Star us on GitHub](https://github.com/MayBind/maybind-sdk)** | **[🌐 Visit MayBind.com](https://maybind.com)**

*Building the future of digital twins* 🤖✨

</div>
