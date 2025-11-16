from django.contrib import admin
from django.db.models import Count
from .models import LottoRound, LottoTicket, WinningResult

@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'draw_date', 'winning_numbers', 'bonus_number', 'is_drawn', 'ticket_sales_count')
    list_filter = ('is_drawn',)
    actions = ['conduct_draw', 'check_winners']

    @admin.display(description='판매된 티켓 수')
    def ticket_sales_count(self, obj):
        # [관리자 기능] 로또 판매 실적 확인
        return obj.tickets.count()

    @admin.action(description="선택된 회차 추첨 진행")
    def conduct_draw(self, request, queryset):
        # [관리자 기능] 로또 추첨
        for lotto_round in queryset.filter(is_drawn=False):
            lotto_round.draw()
        self.message_user(request, f"추첨이 완료되었습니다.")

    @admin.action(description="선택된 회차 당첨자 확인")
    def check_winners(self, request, queryset):
        # [관리자 기능] 당첨자 확인 (및 WinningResult 생성)
        checked_rounds = []
        for lotto_round in queryset.filter(is_drawn=True):
            win_nums = set(map(int, lotto_round.winning_numbers.split(',')))
            bonus_num = lotto_round.bonus_number
            
            for ticket in lotto_round.tickets.all():
                # 이미 확인된 티켓은 건너뜀
                if WinningResult.objects.filter(ticket=ticket).exists():
                    continue

                ticket_nums = set(map(int, ticket.numbers.split(',')))
                match_count = len(win_nums.intersection(ticket_nums))
                
                rank = 0 # 0 = 꽝
                if match_count == 6:
                    rank = 1
                elif match_count == 5 and bonus_num in ticket_nums:
                    rank = 2
                elif match_count == 5:
                    rank = 3
                elif match_count == 4:
                    rank = 4
                elif match_count == 3:
                    rank = 5
                
                WinningResult.objects.create(ticket=ticket, rank=rank)
            
            checked_rounds.append(str(lotto_round.round_number))
        
        if checked_rounds:
            self.message_user(request, f"{', '.join(checked_rounds)}회차 당첨 확인이 완료되었습니다.")
        else:
            self.message_user(request, "추첨이 완료된 회차만 당첨자를 확인할 수 있습니다.", 'warning')

@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'lotto_round', 'numbers', 'is_auto', 'created_at')
    list_filter = ('lotto_round', 'is_auto')
    search_fields = ('user__username',)

@admin.register(WinningResult)
class WinningResultAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_round', 'rank', 'get_ticket_numbers')
    list_filter = ('rank',)
    
    @admin.display(description='사용자')
    def get_username(self, obj):
        return obj.ticket.user.username

    @admin.display(description='회차')
    def get_round(self, obj):
        return obj.ticket.lotto_round

    @admin.display(description='구매 번호')
    def get_ticket_numbers(self, obj):
        return obj.ticket.numbers