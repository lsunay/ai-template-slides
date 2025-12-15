import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .parser import create_client, PresentationStructure
from .renderer import PresentationRenderer

app = typer.Typer(
    name="kimi-cli",
    help="AI-powered PowerPoint presentation generator",
    rich_markup_mode="rich"
)
console = Console()


def read_input(input_path: Optional[str]) -> str:
    """Read input from file or stdin."""
    if input_path and input_path != "-":
        # Read from file
        file_path = Path(input_path)
        if not file_path.exists():
            console.print(f"[red]Error: Input file '{input_path}' not found[/red]")
            raise typer.Exit(1)
        return file_path.read_text(encoding="utf-8")
    else:
        # Read from stdin
        if sys.stdin.isatty():
            console.print("[yellow]Reading from stdin (press Ctrl+D to finish):[/yellow]")
        return sys.stdin.read()


def load_template(template_path: str) -> dict:
    """Load template configuration from JSON file."""
    template_file = Path(template_path)
    if not template_file.exists():
        # Try to find in content_templates directory
        template_file = Path("content_templates") / f"{template_path}.json"
        if not template_file.exists():
            console.print(f"[red]Error: Template '{template_path}' not found[/red]")
            raise typer.Exit(1)
    
    import json
    return json.loads(template_file.read_text(encoding="utf-8"))


@app.command()
def generate(
    input_path: Optional[str] = typer.Argument(
        None,
        help="Path to input text file (use '-' for stdin)",
        show_default=False
    ),
    template: str = typer.Option(
        "academic",
        "--template", "-t",
        help="Template to use (academic, pitch_deck, sales, or path to JSON file)"
    ),
    model: str = typer.Option(
        "openai",
        "--model", "-m",
        help="AI model to use (openai, ollama, lmstudio)"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help="API key for the model (can also use environment variables)"
    ),
    base_url: Optional[str] = typer.Option(
        None,
        "--base-url",
        help="Base URL for the model API (for local models)"
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (.pptx) or '-' for stdout (base64)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output"
    )
):
    """Generate a PowerPoint presentation from input text."""
    
    # Read input
    if verbose:
        console.print(f"[blue]Reading input from {'stdin' if input_path == '-' else input_path or 'stdin'}...[/blue]")
    
    input_text = read_input(input_path)
    if not input_text.strip():
        console.print("[red]Error: Input text is empty[/red]")
        raise typer.Exit(1)
    
    if verbose:
        console.print(f"[green]✓[/green] Read {len(input_text)} characters")
    
    # Load template
    if verbose:
        console.print(f"[blue]Loading template '{template}'...[/blue]")
    
    try:
        template_config = load_template(template)
        if verbose:
            console.print(f"[green]✓[/green] Template loaded successfully")
    except Exception as e:
        console.print(f"[red]Error loading template: {e}[/red]")
        raise typer.Exit(1)
    
    # Create AI client
    if verbose:
        console.print(f"[blue]Initializing {model} client...[/blue]")
    
    try:
        client = create_client(model, api_key=api_key, base_url=base_url)
        if verbose:
            console.print(f"[green]✓[/green] Client initialized")
    except Exception as e:
        console.print(f"[red]Error initializing client: {e}[/red]")
        raise typer.Exit(1)
    
    # Generate presentation structure
    if verbose:
        console.print("[blue]Generating presentation structure...[/blue]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Generating presentation...", total=None)
            structure = client.generate_presentation(input_text, template_config)
        
        if verbose:
            console.print(f"[green]✓[/green] Generated {len(structure.slides)} slides")
    except Exception as e:
        console.print(f"[red]Error generating presentation: {e}[/red]")
        raise typer.Exit(1)
    
    # Render presentation
    if verbose:
        console.print("[blue]Rendering PowerPoint presentation...[/blue]")
    
    try:
        renderer = PresentationRenderer()
        presentation = renderer.render_presentation(structure)
        
        if verbose:
            console.print(f"[green]✓[/green] Presentation rendered")
    except Exception as e:
        console.print(f"[red]Error rendering presentation: {e}[/red]")
        raise typer.Exit(1)
    
    # Output presentation
    if output == "-":
        # Output to stdout as base64
        if verbose:
            console.print("[blue]Encoding presentation to base64...[/blue]")
        
        try:
            base64_data = renderer.to_base64()
            print(base64_data)
            
            if verbose:
                console.print(f"[green]✓[/green] Base64 output complete ({len(base64_data)} characters)")
        except Exception as e:
            console.print(f"[red]Error encoding presentation: {e}[/red]")
            raise typer.Exit(1)
    else:
        # Save to file
        output_path = Path(output or "presentation.pptx")
        
        if verbose:
            console.print(f"[blue]Saving presentation to {output_path}...[/blue]")
        
        try:
            renderer.save_to_file(str(output_path))
            console.print(f"[green]✓[/green] Presentation saved to {output_path}")
        except Exception as e:
            console.print(f"[red]Error saving presentation: {e}[/red]")
            raise typer.Exit(1)


@app.command()
def templates():
    """List available templates."""
    templates_dir = Path("content_templates")
    if not templates_dir.exists():
        console.print("[yellow]No templates directory found[/yellow]")
        return
    
    template_files = list(templates_dir.glob("*.json"))
    if not template_files:
        console.print("[yellow]No templates found[/yellow]")
        return
    
    console.print("[bold]Available templates:[/bold]")
    for template_file in template_files:
        template_name = template_file.stem
        console.print(f"  • {template_name}")


@app.command()
def models():
    """List supported AI models."""
    console.print("[bold]Supported models:[/bold]")
    console.print("  • openai    - OpenAI GPT models (requires API key)")
    console.print("  • ollama    - Local Ollama models")
    console.print("  • lmstudio  - Local LM Studio models")


if __name__ == "__main__":
    app()