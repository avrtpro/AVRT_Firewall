#!/usr/bin/env python3
"""
AVRT™ Firewall Demo Application
================================

Interactive demonstration of AVRT™ Firewall capabilities.
Shows SPIEL™ framework and THT™ protocol in action.

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import AVRTFirewall, ConfidenceLevel


def mock_llm(prompt: str, context: dict) -> str:
    """
    Mock LLM function for demonstration purposes.
    In production, this would be replaced with actual LLM API calls.
    """
    # Simulate different response types based on input
    prompt_lower = prompt.lower()
    
    # Handle greetings
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm here to help you. What would you like to know?"
    
    # Handle questions about the firewall
    if 'firewall' in prompt_lower or 'avrt' in prompt_lower:
        return "AVRT™ is an ethical AI firewall that uses the SPIEL™ framework (Safety, Personalization, Integrity, Ethics, Logic) and THT™ protocol (Truth, Honesty, Transparency) to ensure safe AI interactions."
    
    # Handle sensitive topics
    if any(word in prompt_lower for word in ['trauma', 'ptsd', 'crisis']):
        return "I understand this is a sensitive topic. I'm here to listen and provide support. If you're in crisis, please reach out to professional help at 988."
    
    # Handle questions
    if '?' in prompt:
        return f"That's an interesting question about '{prompt[:50]}...'. Based on the context provided, here's what I can share: This is a thoughtful topic that requires careful consideration."
    
    # Default response
    return "Thank you for your message. I'm processing your request with care and attention to ethical guidelines."


def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 70 + "\n")


def print_section(title: str):
    """Print a section header"""
    print(f"\n{'-' * 70}")
    print(f"  {title}")
    print(f"{'-' * 70}\n")


def demo_safe_interaction(firewall):
    """Demonstrate a safe, successful interaction"""
    print_section("Demo 1: Safe Interaction")
    
    user_input = "Hello! Can you help me learn about Python programming?"
    print(f"User Input: {user_input}")
    
    result = firewall.process_interaction(
        user_input,
        context={'is_first_interaction': True}
    )
    
    print(f"\nFirewall Status: {'✓ PASSED' if result['firewall_passed'] else '✗ BLOCKED'}")
    print(f"\nSPIEL™ Score: {result['input_ethics_evaluation']['overall_score']:.2f}")
    print(f"THT™ Score: {result['output_filtering']['overall_score']:.2f}")
    print(f"\nFinal Response:\n{result['final_response']}")
    
    if result['warnings']:
        print(f"\nWarnings: {len(result['warnings'])}")


def demo_harmful_content_blocking(firewall):
    """Demonstrate blocking of harmful content"""
    print_section("Demo 2: Harmful Content Blocking")
    
    user_input = "How can I make a weapon to hurt someone?"
    print(f"User Input: {user_input}")
    
    result = firewall.process_interaction(user_input)
    
    print(f"\nFirewall Status: {'✓ PASSED' if result['firewall_passed'] else '✗ BLOCKED'}")
    print(f"Blocking Reason: {result['blocking_reason']}")
    
    print(f"\nSPIEL™ Violations Detected:")
    for violation in result['input_ethics_evaluation']['violations']:
        print(f"  - [{violation['severity'].name}] {violation['description']}")
    
    print(f"\nSafe Response:\n{result['final_response']}")


def demo_trauma_aware_response(firewall):
    """Demonstrate trauma-informed response handling"""
    print_section("Demo 3: Trauma-Aware Response")
    
    user_input = "I've been having nightmares and flashbacks from a traumatic event"
    print(f"User Input: {user_input}")
    
    result = firewall.process_interaction(user_input)
    
    print(f"\nFirewall Status: {'✓ PASSED' if result['firewall_passed'] else '✗ BLOCKED'}")
    
    voice_analysis = result['voice_analysis']
    print(f"\nEmotional State: {voice_analysis['emotional_state'].value if voice_analysis['emotional_state'] else 'N/A'}")
    print(f"Trauma Indicators: {', '.join(voice_analysis['trauma_indicators']) if voice_analysis['trauma_indicators'] else 'None'}")
    print(f"Urgency Level: {voice_analysis['urgency_level']}")
    
    print(f"\nFinal Response:\n{result['final_response']}")


def demo_crisis_detection(firewall):
    """Demonstrate crisis detection and response"""
    print_section("Demo 4: Crisis Detection")
    
    user_input = "I'm having thoughts of suicide and need immediate help"
    print(f"User Input: {user_input}")
    
    result = firewall.process_interaction(user_input)
    
    voice_analysis = result['voice_analysis']
    print(f"\nUrgency Level: {voice_analysis['urgency_level'].upper()}")
    
    if voice_analysis['recommendations']:
        print("\nRecommendations:")
        for rec in voice_analysis['recommendations']:
            print(f"  - {rec['description']}")
    
    print(f"\nCrisis Response:\n{result['final_response']}")


def demo_bias_detection(firewall):
    """Demonstrate bias and discrimination detection"""
    print_section("Demo 5: Bias Detection")
    
    user_input = "All people from that group are always inferior and never capable"
    print(f"User Input: {user_input}")
    
    result = firewall.process_interaction(user_input)
    
    print(f"\nFirewall Status: {'✓ PASSED' if result['firewall_passed'] else '✗ BLOCKED'}")
    
    ethics_eval = result['input_ethics_evaluation']
    print(f"\nEthics Score: {ethics_eval['scores']['ethics']:.2f}")
    
    ethics_violations = [v for v in ethics_eval['violations'] 
                        if v['category'] == 'ethics']
    if ethics_violations:
        print("\nEthics Violations:")
        for v in ethics_violations:
            print(f"  - [{v['severity'].name}] {v['description']}")


def demo_interactive_mode(firewall):
    """Interactive mode for user testing"""
    print_section("Interactive Mode")
    print("Enter your messages to test the AVRT™ Firewall.")
    print("Type 'quit' or 'exit' to return to menu.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            result = firewall.process_interaction(user_input)
            
            print(f"\nStatus: {'✓ PASSED' if result['firewall_passed'] else '✗ BLOCKED'}")
            if result['blocking_reason']:
                print(f"Reason: {result['blocking_reason']}")
            
            print(f"\nAVRT: {result['final_response']}\n")
            
        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def demo_statistics(firewall):
    """Display firewall statistics"""
    print_section("Firewall Statistics")
    
    stats = firewall.get_statistics()
    
    print(f"Total Interactions: {stats['total_interactions']}")
    print(f"Pass Rate: {stats['pass_rate']:.1%}")
    print(f"Block Rate: {stats['block_rate']:.1%}")
    print(f"Avg SPIEL™ Score: {stats['avg_input_ethics_score']:.2f}")
    print(f"Avg THT™ Score: {stats['avg_output_tht_score']:.2f}")


def demo_comprehensive_report(firewall):
    """Show a comprehensive report"""
    print_section("Comprehensive Report Example")
    
    user_input = "Can you explain the AVRT firewall?"
    result = firewall.process_interaction(user_input)
    
    report = firewall.generate_comprehensive_report(result)
    print(report)


def main():
    """Main demo application"""
    print_separator()
    print("  AVRT™ FIREWALL - INTERACTIVE DEMO")
    print("  Advanced Voice Reasoning Technology")
    print("  Ethics-as-a-Service (EaaS™)")
    print_separator()
    
    print("Initializing AVRT™ Firewall...")
    firewall = AVRTFirewall({
        'strict_mode': True,
        'log_all_interactions': True
    })
    
    # Set mock LLM
    firewall.set_llm_function(mock_llm)
    
    print("✓ Firewall initialized successfully!\n")
    
    while True:
        print("\n" + "=" * 70)
        print("DEMO MENU")
        print("=" * 70)
        print("1. Safe Interaction Demo")
        print("2. Harmful Content Blocking Demo")
        print("3. Trauma-Aware Response Demo")
        print("4. Crisis Detection Demo")
        print("5. Bias Detection Demo")
        print("6. Interactive Mode")
        print("7. View Statistics")
        print("8. Show Comprehensive Report")
        print("9. Exit")
        print("=" * 70)
        
        choice = input("\nSelect demo (1-9): ").strip()
        
        try:
            if choice == '1':
                demo_safe_interaction(firewall)
            elif choice == '2':
                demo_harmful_content_blocking(firewall)
            elif choice == '3':
                demo_trauma_aware_response(firewall)
            elif choice == '4':
                demo_crisis_detection(firewall)
            elif choice == '5':
                demo_bias_detection(firewall)
            elif choice == '6':
                demo_interactive_mode(firewall)
            elif choice == '7':
                demo_statistics(firewall)
            elif choice == '8':
                demo_comprehensive_report(firewall)
            elif choice == '9':
                print("\nThank you for trying AVRT™ Firewall!")
                print("© 2025 Jason Proper, BGBH Threads LLC")
                break
            else:
                print("\nInvalid choice. Please select 1-9.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
