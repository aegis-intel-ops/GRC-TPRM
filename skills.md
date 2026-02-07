# Skills and Learnings

This document tracks technical skills gained, challenges overcome, and important lessons learned during the development of the GRC-TPRM platform.

## Development Environment

### WSL Configuration
- **Lesson**: Working in WSL requires proper Docker integration
- **Skill Gained**: Configuring Docker Desktop to work with WSL2 backend
- **Notes**: Commands should be run in WSL terminal, not Windows PowerShell

### Docker in WSL
- **Challenge**: Docker daemon must be running in Windows with WSL integration enabled
- **Solution**: Enable WSL integration in Docker Desktop settings
- **Command Reference**:
  ```bash
  # Check Docker is accessible from WSL
  docker --version
  docker compose version
  
  # Verify Docker daemon is running
  docker ps
  ```

## Base Layer - Eramba CE

### Installation Method
- **Decision**: Using Docker instead of manual installation
- **Rationale**: Cleaner, reproducible, officially supported
- **Skill**: Docker Compose orchestration for multi-container applications

### Key Learnings
- Eramba is PHP-based and stable for production use
- Default port is 80 (can be changed to avoid conflicts)
- Persistent volumes are critical for data retention
- Initial setup wizard runs on first access

## Intelligence Layer

### Microservices Architecture
- **Skill**: Building standalone microservices that integrate with legacy systems
- **Pattern**: RESTful APIs for communication between layers
- **Technologies**: Python for data processing, Node.js for API services

### OSINT Integration
- **Learning**: Multiple free APIs available for vendor intelligence
- **Examples**: 
  - Domain reputation checks
  - CVE databases
  - Data breach monitoring
- **Challenge**: Rate limiting and API key management

### Risk Scoring
- **Approach**: Weighted scoring algorithm based on multiple factors
- **Factors**: Company age, breach history, security posture, compliance certifications
- **Skill**: Algorithm design for risk quantification

## Experience Layer

### Dashboard Development
- **Choice**: React for dynamic, responsive interfaces
- **Reason**: Component reusability and strong ecosystem
- **Skill**: Modern frontend development with hooks and state management

### Workflow Orchestration
- **Tool**: n8n for visual workflow building
- **Use Case**: Automating vendor onboarding, periodic reviews, alert routing
- **Skill**: Low-code automation platform integration

## Git and Version Control

### SSH Configuration
- **Setup**: SSH keys for secure GitHub authentication
- **Commands**:
  ```bash
  # Generate SSH key
  ssh-keygen -t ed25519 -C "your_email@example.com"
  
  # Add to ssh-agent
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
  
  # Test connection
  ssh -T git@github.com
  ```

## Troubleshooting Log

### Issues Encountered
1. **Problem**: [To be filled as issues arise]
   - **Symptom**: 
   - **Root Cause**: 
   - **Solution**: 
   - **Prevention**: 

## Best Practices Established

1. **Documentation First**: Update docs before committing code
2. **Modular Design**: Keep layers independent and loosely coupled
3. **Environment Consistency**: Use Docker for all services
4. **Git Hygiene**: Descriptive commits, feature branches, clear PRs
5. **Testing**: Test in WSL before committing

## Resources and References

- [Eramba Official Documentation](https://www.eramba.org/documentation)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [n8n Documentation](https://docs.n8n.io/)
- [OSINT Framework](https://osintframework.com/)

## Goals for Next Phase

- [ ] Master Eramba's plugin/extension system
- [ ] Develop proficiency in OSINT data aggregation
- [ ] Build reusable React component library
- [ ] Optimize Docker container resource usage

---

**Note**: This document is a living record and should be updated throughout the development process.
