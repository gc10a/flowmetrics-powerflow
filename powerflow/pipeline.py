"""
Core pipeline functionality for PowerFlow.
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
import logging

# Optional rich support for better output
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.logging import RichHandler
    HAS_RICH = True
    
    # Setup logging with rich
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
except ImportError:
    HAS_RICH = False
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

logger = logging.getLogger("powerflow")

# Create console (or mock if rich not available)
if HAS_RICH:
    console = Console()
else:
    class MockConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = MockConsole()


class PipelineContext:
    """Context object passed through pipeline stages."""
    
    def __init__(self, initial_data: Optional[List[Dict[str, Any]]] = None):
        self.data: List[Dict[str, Any]] = initial_data or []
        self.metadata: Dict[str, Any] = {
            "start_time": datetime.now(),
            "stages_completed": [],
            "record_count": 0,
        }
        self.errors: List[Dict[str, Any]] = []
    
    def add_error(self, stage: str, error: Exception, record: Optional[Dict] = None) -> None:
        """Add an error to the context."""
        self.errors.append({
            "stage": stage,
            "error": str(error),
            "record": record,
            "timestamp": datetime.now(),
        })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline execution statistics."""
        return {
            "start_time": self.metadata["start_time"],
            "end_time": datetime.now(),
            "duration": (datetime.now() - self.metadata["start_time"]).total_seconds(),
            "stages_completed": len(self.metadata["stages_completed"]),
            "record_count": len(self.data),
            "error_count": len(self.errors),
        }


class PipelineStage:
    """Base class for pipeline stages."""
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
    
    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute this stage of the pipeline."""
        raise NotImplementedError("Subclasses must implement execute()")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"


class Pipeline:
    """
    A data pipeline for revenue operations workflows.
    
    Example:
        >>> pipeline = Pipeline(name="Deal Pipeline")
        >>> pipeline.add_stage(SalesforceSource())
        >>> pipeline.add_stage(FilterTransformer(lambda x: x['amount'] > 10000))
        >>> pipeline.add_stage(CSVDestination("high_value_deals.csv"))
        >>> result = pipeline.run()
    """
    
    def __init__(self, name: str = "Pipeline", fail_fast: bool = False):
        self.name = name
        self.fail_fast = fail_fast
        self.stages: List[PipelineStage] = []
        self.hooks: Dict[str, List[Callable]] = {
            "pre_run": [],
            "post_run": [],
            "pre_stage": [],
            "post_stage": [],
        }
    
    def add_stage(self, stage: PipelineStage) -> "Pipeline":
        """Add a stage to the pipeline."""
        self.stages.append(stage)
        return self
    
    def add_hook(self, hook_type: str, callback: Callable) -> "Pipeline":
        """Add a hook callback."""
        if hook_type not in self.hooks:
            raise ValueError(f"Invalid hook type: {hook_type}")
        self.hooks[hook_type].append(callback)
        return self
    
    def run(self, initial_data: Optional[List[Dict[str, Any]]] = None) -> PipelineContext:
        """
        Run the pipeline.
        
        Args:
            initial_data: Optional initial data to seed the pipeline
            
        Returns:
            PipelineContext with results and metadata
        """
        context = PipelineContext(initial_data)
        
        # Execute pre-run hooks
        for hook in self.hooks["pre_run"]:
            hook(self, context)
        
        if HAS_RICH:
            console.print(f"\n[bold blue]🚀 Starting Pipeline: {self.name}[/bold blue]")
        else:
            print(f"\n🚀 Starting Pipeline: {self.name}")
        
        if HAS_RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
            ) as progress:
                task = progress.add_task("Processing...", total=len(self.stages))
                
                for i, stage in enumerate(self.stages):
                    progress.update(task, description=f"Stage {i+1}/{len(self.stages)}: {stage.name}")
                    self._execute_stage(context, stage)
                    progress.advance(task)
        else:
            # Simple progress without rich
            for i, stage in enumerate(self.stages):
                print(f"Stage {i+1}/{len(self.stages)}: {stage.name}")
                self._execute_stage(context, stage)
        
        # Execute post-run hooks
        for hook in self.hooks["post_run"]:
            hook(self, context)
        
        # Print summary
        stats = context.get_stats()
        if HAS_RICH:
            console.print("\n[bold green]✅ Pipeline Complete[/bold green]")
            console.print(f"Duration: {stats['duration']:.2f}s")
            console.print(f"Records processed: {stats['record_count']}")
            console.print(f"Errors: {stats['error_count']}")
            
            if context.errors:
                console.print("\n[bold yellow]⚠️  Errors encountered:[/bold yellow]")
                for error in context.errors[:5]:  # Show first 5 errors
                    console.print(f"  - Stage '{error['stage']}': {error['error']}")
                if len(context.errors) > 5:
                    console.print(f"  ... and {len(context.errors) - 5} more")
        else:
            print("\n✅ Pipeline Complete")
            print(f"Duration: {stats['duration']:.2f}s")
            print(f"Records processed: {stats['record_count']}")
            print(f"Errors: {stats['error_count']}")
            
            if context.errors:
                print("\n⚠️  Errors encountered:")
                for error in context.errors[:5]:
                    print(f"  - Stage '{error['stage']}': {error['error']}")
                if len(context.errors) > 5:
                    print(f"  ... and {len(context.errors) - 5} more")
        
        return context
    
    def _execute_stage(self, context: PipelineContext, stage: PipelineStage) -> None:
        """Execute a single pipeline stage."""
        # Execute pre-stage hooks
        for hook in self.hooks["pre_stage"]:
            hook(self, context, stage)
        
        try:
            logger.info(f"Executing stage: {stage.name}")
            context = stage.execute(context)
            context.metadata["stages_completed"].append(stage.name)
            
        except Exception as e:
            logger.error(f"Error in stage {stage.name}: {e}")
            context.add_error(stage.name, e)
            
            if self.fail_fast:
                raise
        
        # Execute post-stage hooks
        for hook in self.hooks["post_stage"]:
            hook(self, context, stage)

