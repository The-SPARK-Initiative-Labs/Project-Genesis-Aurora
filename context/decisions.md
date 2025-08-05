# Aurora Architectural Decisions

## Core Philosophy Decisions

### ADR-001: EQ-First Agent Architecture
**Status**: Accepted  
**Date**: Project inception  
**Decision**: Prioritize emotional intelligence over pure reasoning capability  
**Rationale**: Most AI agents focus on "IQ" (reasoning, planning, tool use). Aurora tests the hypothesis that emotional intelligence as the foundation creates superior AI companionship.  
**Consequences**: 
- Positive: Unique positioning, more human-like interaction
- Negative: More complex to implement and measure

### ADR-002: Architectural Honesty as Core Constraint
**Status**: Accepted  
**Date**: Project inception  
**Decision**: Agent cannot lie, simulate physical actions, or create false narratives  
**Rationale**: Trustworthiness requires structural honesty, not policy-based restrictions  
**Consequences**:
- Positive: Genuine trustworthiness, no roleplay confusion
- Negative: Limits certain interaction patterns

### ADR-003: Local-First Architecture
**Status**: Accepted  
**Date**: Project inception  
**Decision**: Use LM Studio + ChromaDB + local processing exclusively  
**Rationale**: Complete privacy, control, and independence from external services  
**Consequences**:
- Positive: Privacy, customization, no API costs
- Negative: Hardware requirements, maintenance complexity

## Technical Architecture Decisions

### ADR-004: Vertical Integration Over Frameworks
**Status**: Accepted  
**Date**: Master Implementation Plan v3.0  
**Decision**: Build custom A.U.R.A. Engine instead of using LangChain/LangGraph  
**Rationale**: Tight integration between memory, emotion, and reasoning creates superior coherence  
**Consequences**:
- Positive: Optimized for Aurora's specific needs, full control
- Negative: More development effort, no community ecosystem

### ADR-005: Three-Layer Memory System
**Status**: Accepted  
**Date**: Architecture design phase  
**Decision**: Implement Raw Log → Emotional Overlay → Consolidated Core memory  
**Rationale**: Separates objective facts from subjective experience while maintaining complete history  
**Consequences**:
- Positive: Rich memory with emotional context, complete audit trail
- Negative: Storage overhead, complex consolidation process

### ADR-006: Producer-Consumer TTS Architecture
**Status**: Accepted  
**Date**: Voice system implementation  
**Decision**: Use separate threads for audio generation and playback  
**Rationale**: Enables streaming speech without blocking, reduces perceived latency  
**Consequences**:
- Positive: Smooth audio streaming, responsive interaction
- Negative: Threading complexity, harder to debug

### ADR-007: Multi-Agent Memory Consolidation
**Status**: Accepted  
**Date**: Memory system design  
**Decision**: Use Extractor → Validator → Narrative Weaver agent pipeline  
**Rationale**: Ensures only verified facts stored, prevents hallucination in memory  
**Consequences**:
- Positive: High-quality memory, fact verification
- Negative: Complex pipeline, higher processing cost

## Implementation Decisions

### ADR-008: Class-Based Architecture Refactor
**Status**: Accepted  
**Date**: Phase 1 completion  
**Decision**: Migrate from script-based to Aurora class-based design  
**Rationale**: Better organization, resource management, and extensibility  
**Consequences**:
- Positive: Cleaner code, better testing, easier maintenance
- Negative: Migration effort, learning curve

### ADR-009: Pydantic Schema Enforcement
**Status**: Accepted  
**Date**: Structured output implementation  
**Decision**: Use Pydantic models for all LLM outputs in consolidation pipeline  
**Rationale**: Ensures reliable, parseable output from LLM agents  
**Consequences**:
- Positive: Prevents parsing errors, validates data structure
- Negative: Additional complexity, schema maintenance

### ADR-010: Standalone Memory Consolidation
**Status**: Accepted  
**Date**: v4.0 consolidation refactor  
**Decision**: Run memory consolidation as separate script, not integrated in Aurora class  
**Rationale**: Avoids blocking main conversation, allows manual control  
**Consequences**:
- Positive: Non-blocking operation, easier debugging
- Negative: Manual process, requires separate execution

## Development Process Decisions

### ADR-011: AI-Native Development Model
**Status**: Accepted  
**Date**: Project inception  
**Decision**: Use AI collaboration for all coding, Ben as visionary/architect  
**Rationale**: Ben is coding novice but strong conceptual designer  
**Consequences**:
- Positive: Leverages strengths, pioneering new development model
- Negative: Dependency on AI quality, context management challenges

### ADR-012: Comprehensive Testing Strategy
**Status**: Accepted  
**Date**: Phase 1 development  
**Decision**: Create isolated tests for each component before integration  
**Rationale**: Complex system requires systematic validation  
**Consequences**:
- Positive: Reliable components, easier debugging
- Negative: Test maintenance overhead

### ADR-013: Simple Prompting for Memory Consolidation
**Status**: Accepted  
**Date**: 2025-07-16  
**Decision**: Use simple text prompting instead of LM Studio's structured output for memory consolidation agents
**Rationale**: Testing revealed that Nemo-12B model works better with simple prompts than response_format or tool-calling approaches; model-specific capabilities vary  
**Consequences**:
- Positive: Memory consolidation pipeline works reliably, simpler implementation, better model compatibility
- Negative: Less guaranteed structure, requires manual parsing

## Abandoned Paths

### Rejected: LangChain/LangGraph Framework
**Date**: Master Implementation Plan evolution  
**Reason**: Generic framework couldn't provide tight integration needed for EQ-first architecture  
**Learning**: Custom architecture better for specialized requirements

### Rejected: Cloud-Based Processing
**Date**: Architecture planning  
**Reason**: Privacy concerns and dependency on external services  
**Learning**: Local-first approach aligns better with Aurora's independence philosophy

### Rejected: Simple Prompt Engineering
**Date**: Early development  
**Reason**: Insufficient for complex multi-agent memory consolidation  
**Learning**: Structured output with Pydantic schemas essential for reliability

### Rejected: Prompt-Based JSON Generation
**Date**: 2025-07-16  
**Reason**: Consistently produced malformed JSON with parsing errors despite prompt refinement  
**Learning**: Native structured output with response_format is the canonical solution for reliable JSON

### Rejected: LM Studio Structured Output for Nemo-12B
**Date**: 2025-07-16  
**Reason**: Model doesn't reliably support response_format or tool-calling, returned empty responses
**Learning**: Model-specific capabilities vary; simple prompting can be more effective than advanced features
