"""Tests for pipeline functionality."""

import pytest
from powerflow.pipeline import Pipeline, PipelineContext, PipelineStage


class MockStage(PipelineStage):
    """Mock pipeline stage for testing."""
    
    def __init__(self, name="MockStage", should_fail=False):
        super().__init__(name)
        self.executed = False
        self.should_fail = should_fail
    
    def execute(self, context):
        self.executed = True
        if self.should_fail:
            raise ValueError("Mock error")
        context.data.append({"stage": self.name})
        return context


def test_pipeline_context_initialization():
    """Test PipelineContext initialization."""
    context = PipelineContext()
    assert context.data == []
    assert context.metadata["record_count"] == 0
    assert len(context.errors) == 0


def test_pipeline_context_with_initial_data():
    """Test PipelineContext with initial data."""
    initial_data = [{"id": 1}, {"id": 2}]
    context = PipelineContext(initial_data)
    assert len(context.data) == 2
    assert context.data == initial_data


def test_pipeline_context_add_error():
    """Test adding errors to context."""
    context = PipelineContext()
    error = ValueError("Test error")
    context.add_error("TestStage", error, {"id": 1})
    
    assert len(context.errors) == 1
    assert context.errors[0]["stage"] == "TestStage"
    assert "Test error" in context.errors[0]["error"]
    assert context.errors[0]["record"] == {"id": 1}


def test_pipeline_context_get_stats():
    """Test getting pipeline statistics."""
    context = PipelineContext([{"id": 1}, {"id": 2}])
    context.metadata["stages_completed"] = ["Stage1", "Stage2"]
    context.add_error("Stage1", ValueError("error"))
    
    stats = context.get_stats()
    assert stats["record_count"] == 2
    assert stats["stages_completed"] == 2
    assert stats["error_count"] == 1
    assert "duration" in stats


def test_pipeline_add_stage():
    """Test adding stages to pipeline."""
    pipeline = Pipeline("Test")
    stage1 = MockStage("Stage1")
    stage2 = MockStage("Stage2")
    
    pipeline.add_stage(stage1).add_stage(stage2)
    
    assert len(pipeline.stages) == 2
    assert pipeline.stages[0] == stage1
    assert pipeline.stages[1] == stage2


def test_pipeline_run():
    """Test running a basic pipeline."""
    pipeline = Pipeline("Test")
    stage1 = MockStage("Stage1")
    stage2 = MockStage("Stage2")
    
    pipeline.add_stage(stage1).add_stage(stage2)
    result = pipeline.run()
    
    assert stage1.executed
    assert stage2.executed
    assert len(result.data) == 2
    assert len(result.metadata["stages_completed"]) == 2


def test_pipeline_with_initial_data():
    """Test pipeline with initial data."""
    pipeline = Pipeline("Test")
    stage = MockStage("Stage")
    pipeline.add_stage(stage)
    
    initial_data = [{"id": 1}, {"id": 2}]
    result = pipeline.run(initial_data)
    
    assert len(result.data) == 3  # 2 initial + 1 from stage


def test_pipeline_fail_fast():
    """Test pipeline with fail_fast enabled."""
    pipeline = Pipeline("Test", fail_fast=True)
    stage1 = MockStage("Stage1", should_fail=True)
    stage2 = MockStage("Stage2")
    
    pipeline.add_stage(stage1).add_stage(stage2)
    
    with pytest.raises(ValueError):
        pipeline.run()
    
    assert stage1.executed
    assert not stage2.executed


def test_pipeline_continue_on_error():
    """Test pipeline continuing after errors."""
    pipeline = Pipeline("Test", fail_fast=False)
    stage1 = MockStage("Stage1", should_fail=True)
    stage2 = MockStage("Stage2")
    
    pipeline.add_stage(stage1).add_stage(stage2)
    result = pipeline.run()
    
    assert stage1.executed
    assert stage2.executed
    assert len(result.errors) == 1
    assert result.errors[0]["stage"] == "Stage1"


def test_pipeline_hooks():
    """Test pipeline hooks."""
    pipeline = Pipeline("Test")
    stage = MockStage("Stage")
    pipeline.add_stage(stage)
    
    pre_run_called = []
    post_run_called = []
    pre_stage_called = []
    post_stage_called = []
    
    pipeline.add_hook("pre_run", lambda p, c: pre_run_called.append(True))
    pipeline.add_hook("post_run", lambda p, c: post_run_called.append(True))
    pipeline.add_hook("pre_stage", lambda p, c, s: pre_stage_called.append(True))
    pipeline.add_hook("post_stage", lambda p, c, s: post_stage_called.append(True))
    
    pipeline.run()
    
    assert len(pre_run_called) == 1
    assert len(post_run_called) == 1
    assert len(pre_stage_called) == 1
    assert len(post_stage_called) == 1


def test_pipeline_hook_invalid_type():
    """Test adding hook with invalid type."""
    pipeline = Pipeline("Test")
    
    with pytest.raises(ValueError):
        pipeline.add_hook("invalid_type", lambda: None)

