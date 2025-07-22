from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from random import choice, randint
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['user_stats'] = {
            'xp': request.user.xp,
            'level': request.user.level,
            'coins': request.user.coins,
            'points': request.user.points,
        }
    return render(request, 'core/home.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def mine_view(request):
    user = request.user
    cooldown, created = MiningCooldown.objects.get_or_create(user=user)
    can_mine = cooldown.can_mine()
    message = ""

    if request.method == "POST" and can_mine:
        tool = UserTool.objects.filter(user=user, equipped=True).first()
        if not tool:
            message = "You must equip a tool before mining!"
        else:
            mined_resource = choice(Resource.objects.all())
            amount = randint(1, 3) * tool.tool.power
            xp_earned = 5 * amount  # XP logic

            inv, _ = Inventory.objects.get_or_create(user=user, resource=mined_resource)
            inv.quantity += amount
            inv.save()

            cooldown.set_next_time(10 / tool.tool.power)

            # Add XP and update leaderboard
            user.gain_xp(xp_earned)
            LeaderboardEntry.objects.update_or_create(user=user, defaults={'total_xp': user.xp})

            message = f"You mined {amount}x {mined_resource.name} and earned {xp_earned} XP!"

    return render(request, 'core/mine.html', {
        "can_mine": can_mine,
        "cooldown_time": cooldown.next_mine_time,
        "message": message
    })


@login_required
def equip_tool(request, tool_id):
    tool_to_equip = UserTool.objects.filter(id=tool_id, user=request.user).first()
    if tool_to_equip:
        # Unequip others
        UserTool.objects.filter(user=request.user).update(equipped=False)
        tool_to_equip.equipped = True
        tool_to_equip.save()
        messages.success(request, f"{tool_to_equip.tool.name} equipped!")
    return redirect('inventory')

@login_required
def inventory_view(request):
    user = request.user
    inventory = Inventory.objects.filter(user=user)
    tools = UserTool.objects.filter(user=user)

    return render(request, 'core/inventory.html', {
        "inventory": inventory,
        "tools": tools
    })

@login_required
def shop_view(request):
    tools = Tool.objects.all()
    inventory = Inventory.objects.filter(user=request.user)
    message = ""

    if request.method == "POST":
        if 'buy_tool' in request.POST:
            tool_id = request.POST['buy_tool']
            tool = Tool.objects.get(id=tool_id)
            if request.user.coins >= tool.cost:
                UserTool.objects.create(user=request.user, tool=tool)
                request.user.coins -= tool.cost
                request.user.save()
                message = f"You bought a {tool.name}!"
            else:
                message = "Not enough coins to buy tool."

        elif 'sell_resource' in request.POST:
            inv_id = request.POST['sell_resource']
            inv = Inventory.objects.get(id=inv_id)
            total_value = inv.quantity * inv.resource.value
            xp_earned = inv.quantity * 2  # XP for selling

            request.user.coins += total_value
            request.user.gain_xp(xp_earned)
            inv.quantity = 0
            request.user.save()
            inv.save()

            LeaderboardEntry.objects.update_or_create(user=request.user, defaults={'total_xp': request.user.xp})

            message = f"Sold all {inv.resource.name} for {total_value} coins and earned {xp_earned} XP!"

    return render(request, 'core/shop.html', {
        'tools': tools,
        'inventory': inventory,
        'message': message
    })

@login_required
def leaderboard_view(request):
    top_users = LeaderboardEntry.objects.select_related('user').order_by('-total_xp')[:10]
    return render(request, 'core/leaderboard.html', {'top_users': top_users})
