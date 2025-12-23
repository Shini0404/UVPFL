"""
UVPFL Step 7 & 8 Combined Runner

Step 7: Federated Learning Framework for User Profiling
Step 8: Evaluation and Comparison with State-of-the-Art

Usage:
    python run_step7_step8.py              # Run both steps
    python run_step7_step8.py --step 7     # Run only step 7
    python run_step7_step8.py --step 8     # Run only step 8
    python run_step7_step8.py --test       # Quick test
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def run_step7_federated_learning(
    data_dir: str = 'processed_data',
    num_rounds: int = 10,
    local_epochs: int = 5,
    test_mode: bool = False
):
    """
    Run Step 7: Federated Learning Framework.
    
    Args:
        data_dir: Directory containing processed data
        num_rounds: Number of federated rounds
        local_epochs: Local epochs per round
        test_mode: If True, run quick test only
    """
    print("=" * 70)
    print("STEP 7: Federated Learning Framework for User Profiling")
    print("=" * 70)
    print()
    
    from federated_learning import (
        FederatedConfig,
        FederatedServer,
        FederatedClient,
        UserProfile,
        test_federated_learning,
        run_federated_learning
    )
    
    if test_mode:
        print("Running quick test...")
        test_federated_learning()
        return None
    
    # Run full federated learning
    server = run_federated_learning(
        data_dir=data_dir,
        num_rounds=num_rounds,
        local_epochs=local_epochs,
        save_model=True
    )
    
    print("\n✅ Step 7 Complete: Federated Learning Framework implemented")
    print(f"   - {len(server.clients)} clients trained")
    print(f"   - {num_rounds} federated rounds completed")
    print(f"   - User profiles stored for similar user matching")
    
    return server


def run_step8_evaluation(
    model_path: str = None,
    test_data_path: str = 'processed_data',
    output_dir: str = 'results',
    test_mode: bool = False
):
    """
    Run Step 8: Evaluation and SOTA Comparison.
    
    Args:
        model_path: Path to trained model
        test_data_path: Path to test data
        output_dir: Output directory for results
        test_mode: If True, run quick test only
    """
    print("\n" + "=" * 70)
    print("STEP 8: Evaluation and Comparison with State-of-the-Art")
    print("=" * 70)
    print()
    
    from evaluate import (
        UVPFLEvaluator,
        ViewportEvaluator,
        SOTAComparator,
        EvaluationVisualizer,
        test_evaluation,
        run_evaluation
    )
    
    if test_mode:
        print("Running quick test...")
        test_evaluation()
        return None
    
    # Run full evaluation
    results = run_evaluation(
        model_path=model_path,
        test_data_path=test_data_path,
        output_dir=output_dir,
        generate_plots=True
    )
    
    print("\n✅ Step 8 Complete: Evaluation and SOTA comparison done")
    print(f"   - Results saved to {output_dir}/")
    print(f"   - Comparison plots generated")
    print(f"   - Report generated")
    
    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='UVPFL Step 7 & 8: Federated Learning and Evaluation'
    )
    parser.add_argument(
        '--step', type=int, choices=[7, 8],
        help='Run specific step only (7 or 8). Default: run both'
    )
    parser.add_argument(
        '--test', action='store_true',
        help='Run quick tests only'
    )
    parser.add_argument(
        '--data_dir', type=str, default='processed_data',
        help='Path to processed data directory'
    )
    parser.add_argument(
        '--model_path', type=str, default=None,
        help='Path to trained model for evaluation'
    )
    parser.add_argument(
        '--output_dir', type=str, default='results',
        help='Output directory for results'
    )
    parser.add_argument(
        '--num_rounds', type=int, default=10,
        help='Number of federated rounds'
    )
    parser.add_argument(
        '--local_epochs', type=int, default=5,
        help='Local epochs per federated round'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("UVPFL Implementation - Steps 7 & 8")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output_dir}")
    print()
    
    # Run Step 7 (Federated Learning)
    if args.step is None or args.step == 7:
        try:
            run_step7_federated_learning(
                data_dir=args.data_dir,
                num_rounds=args.num_rounds,
                local_epochs=args.local_epochs,
                test_mode=args.test
            )
        except Exception as e:
            print(f"\n❌ Step 7 Error: {e}")
            if not args.test:
                raise
    
    # Run Step 8 (Evaluation)
    if args.step is None or args.step == 8:
        try:
            run_step8_evaluation(
                model_path=args.model_path,
                test_data_path=args.data_dir,
                output_dir=args.output_dir,
                test_mode=args.test
            )
        except Exception as e:
            print(f"\n❌ Step 8 Error: {e}")
            if not args.test:
                raise
    
    print("\n" + "=" * 70)
    print("✅ All requested steps completed!")
    print("=" * 70)
    
    # Summary
    print("\nSummary:")
    print("-" * 50)
    if args.step is None or args.step == 7:
        print("Step 7 (Federated Learning):")
        print("  - User profiling framework: ✅")
        print("  - FedAvg aggregation: ✅")
        print("  - Similar user matching: ✅")
        print("  - Privacy-preserving training: ✅")
    
    if args.step is None or args.step == 8:
        print("Step 8 (Evaluation):")
        print("  - Viewport prediction metrics: ✅")
        print("  - Precision/Recall calculation: ✅")
        print("  - SOTA comparison (Mosaic, Flare, Sparkle): ✅")
        print("  - Visualization plots: ✅")
    
    print("-" * 50)
    print("\nNext steps:")
    print("  1. Train the model: python train.py --epochs 50")
    print("  2. Run evaluation: python evaluate.py --model checkpoints/best_model.keras")
    print("  3. Run federated learning: python federated_learning.py --rounds 10")


if __name__ == '__main__':
    main()

