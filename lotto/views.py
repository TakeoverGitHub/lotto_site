from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LottoRound, LottoTicket, WinningResult
from django.utils import timezone
import random

@login_required
def lotto_index(request):
    """메인 페이지. 현재 진행 중인 회차와 내 티켓 목록 보여주기"""
    
    # 현재 진행중인(아직 추첨 안 한) 마지막 회차 찾기
    current_round = LottoRound.objects.filter(is_drawn=False).order_by('-round_number').first()
    
    # 내 티켓 목록
    my_tickets = LottoTicket.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    context = {
        'current_round': current_round,
        'my_tickets': my_tickets,
    }
    return render(request, 'lotto/lotto_index.html', context) # 이 HTML 파일은 직접 만드셔야 합니다.

@login_required
def buy_lotto(request):
    """[사용자 기능] 로또 구매 (수동/자동)"""
    
    current_round = LottoRound.objects.filter(is_drawn=False).order_by('-round_number').first()
    if not current_round:
        messages.error(request, "현재 구매 가능한 회차가 없습니다.")
        return redirect('lotto_index') # lotto_index는 urls.py에서 정의할 이름

    if request.method == 'POST':
        buy_type = request.POST.get('buy_type') # 'auto' or 'manual'
        
        try:
            if buy_type == 'auto':
                numbers = LottoTicket.generate_auto_numbers()
                LottoTicket.objects.create(
                    user=request.user,
                    lotto_round=current_round,
                    numbers=numbers,
                    is_auto=True
                )
                messages.success(request, f"자동 번호({numbers}) 구매가 완료되었습니다.")
            
            elif buy_type == 'manual':
                # HTML 폼에서 'num1', 'num2'... 6개의 입력을 받는다고 가정
                manual_nums = []
                for i in range(1, 7):
                    num_str = request.POST.get(f'num{i}')
                    if not num_str:
                        raise ValueError("6개의 번호를 모두 입력해야 합니다.")
                    num = int(num_str)
                    if not (1 <= num <= 45):
                        raise ValueError("번호는 1과 45 사이여야 합니다.")
                    if num in manual_nums:
                        raise ValueError("중복된 번호를 입력할 수 없습니다.")
                    manual_nums.append(num)
                
                numbers = ",".join(map(str, sorted(manual_nums)))
                LottoTicket.objects.create(
                    user=request.user,
                    lotto_round=current_round,
                    numbers=numbers,
                    is_auto=False
                )
                messages.success(request, f"수동 번호({numbers}) 구매가 완료되었습니다.")
            
            else:
                raise ValueError("알 수 없는 구매 방식입니다.")

        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"구매 중 오류가 발생했습니다: {e}")
        
        return redirect('lotto_index')

    # GET 요청 시
    return render(request, 'lotto/buy_lotto.html', {'current_round': current_round}) # 이 HTML 파일은 직접 만드셔야 합니다.


@login_required
def check_winnings(request):
    """[사용자 기능] 내 당첨 확인 페이지"""
    
    # admin에서 '당첨자 확인'을 실행해야 WinningResult가 생성됨
    my_results = WinningResult.objects.filter(ticket__user=request.user).order_by('-ticket__lotto_round__round_number')
    
    return render(request, 'lotto/check_winnings.html', {'my_results': my_results}) # 이 HTML 파일은 직접 만드셔야 합니다.