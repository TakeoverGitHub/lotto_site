from django.db import models
from django.conf import settings
from django.utils import timezone
import random

class LottoRound(models.Model):
    """로또 회차 정보"""
    round_number = models.PositiveIntegerField(unique=True, help_text="회차 번호")
    draw_date = models.DateTimeField(null=True, blank=True, help_text="추첨일")
    winning_numbers = models.CharField(max_length=100, blank=True, help_text="당첨 번호 (쉼표로 구분)")
    bonus_number = models.PositiveSmallIntegerField(null=True, blank=True, help_text="보너스 번호")
    is_drawn = models.BooleanField(default=False, help_text="추첨 완료 여부")

    def __str__(self):
        return f"{self.round_number}회차"

    def draw(self):
        """[관리자 기능] 당첨 번호 및 보너스 번호 추첨"""
        if not self.is_drawn:
            numbers = random.sample(range(1, 46), 7)
            self.winning_numbers = ",".join(map(str, sorted(numbers[:6])))
            self.bonus_number = numbers[6]
            self.draw_date = timezone.now()
            self.is_drawn = True
            self.save()

class LottoTicket(models.Model):
    """사용자가 구매한 로또 티켓"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    lotto_round = models.ForeignKey(LottoRound, on_delete=models.CASCADE, related_name="tickets")
    numbers = models.CharField(max_length=100, help_text="선택한 번호 (쉼표로 구분, 정렬됨)")
    is_auto = models.BooleanField(default=False, help_text="자동 생성 여부")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lotto_round}회차"

    @staticmethod
    def generate_auto_numbers():
        """[사용자 기능] 자동 번호 6개 생성"""
        auto_nums = random.sample(range(1, 46), 6)
        return ",".join(map(str, sorted(auto_nums)))

class WinningResult(models.Model):
    """당첨 결과 (추첨 후 생성됨)"""
    ticket = models.OneToOneField(LottoTicket, on_delete=models.CASCADE, primary_key=True)
    rank = models.PositiveSmallIntegerField(help_text="당첨 등수 (1~5, 0은 꽝)")
    
    def __str__(self):
        return f"{self.ticket} - {self.rank}등"