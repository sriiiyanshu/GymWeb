import re
from django.utils.timezone import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from hello.forms import LogMessageForm
from hello.models import LogMessage, WorkoutHistory
from django.views.generic import ListView
import os
import json


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")


# Add this code elsewhere in the file:
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})

# Dictionary mapping exercise names to their media files
EXERCISE_IMAGES = {
    'Barbell Bench Press': 'Bench-press-barbell.mp4',
    'Incline Dumbbell Press': 'incline-dumbell-press.mp4',
    'Cable Flyes': 'cable-flyes.mp4',
    'Tricep Pushdowns': 'tricep-pushdown.jpg',
    'Overhead Dumbbell Extension': 'overhead-rope-extension.webp',
    'Tricep Kickbacks': 'Triceps-Kickback.mp4',
    'Pull-ups': 'Pull-ups.mp4',
    'Barbell Rows': 'barbell-row.webp',
    'Lat Pulldowns': 'lat-pulldown.mp4',
    'Dumbbell Bicep Curls': 'bicep-curl.mp4',
    'Hammer Curls': 'hammer-curl.mp4',
    'Concentration Curls': 'concentartion-curls.mp4',
    'Squats': 'squats.webp',
    'Leg Press': 'leg-press.mp4',
    'Lunges': 'lunges.mp4',
    'Leg Extensions': 'leg-extension.png',
    'Leg Curls': 'leg-curls.mp4',
    'Calf Raises': 'calf-raise.mp4',
    'Dumbbell Shoulder Press': 'shoulder-press.gif',
    'Lateral Raises': 'lateral-raises.webp',
    'Rear Delt Flyes': 'rear-delt-fly.webp',
    'Hanging Leg Raises': 'hanging-leg-raise.webp',
    'Planks': 'plank.gif',
    'Russian Twists': 'russian-twists.mp4',
    'Incline Bench Press': 'incline-bench-press.mp4',
    'Tricep Dips': 'tricep-dips.webp',
    'Overhead Rope Extensions': 'Tricep-extension.png',
    'Preacher Curls': 'preacher-curl.webp',
    'Deadlifts': 'deadlift.mp4',
    'Dumbbell Chest Press': 'incline-dumbell-press.mp4',
    'Cable Crossovers': 'cable-flyes.mp4',

}

# Hardcoded fitness routines data
fitness_routines = [
    {
        'id': 1,
        'title': 'Day 1: Chest and Triceps',
        'exercises': [
            {
                'name': 'Barbell Bench Press',
                'sets': 4,
                'reps': '8-12',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Incline Dumbbell Press',
                'sets': 3,
                'reps': '10-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Cable Flyes',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Tricep Pushdowns',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Overhead Dumbbell Extension',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Tricep Kickbacks',
                'sets': 3,
                'reps': '8-10',
                'duration': 40,
                'image_placeholder': True
            }
        ]
    },
    {
        'id': 2,
        'title': 'Day 2: Back and Biceps',
        'exercises': [
            {
                'name': 'Pull-ups',
                'sets': 3,
                'reps': '8-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Barbell Rows',
                'sets': 4,
                'reps': '8-12',
                'duration': 50,
                'image_placeholder': True
            },
            {
                'name': 'Lat Pulldowns',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Dumbbell Bicep Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Hammer Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Preacher Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            }
        ]
    },
    {
        'id': 3,
        'title': 'Day 3: Legs',
        'exercises': [
            {
                'name': 'Squats',
                'sets': 4,
                'reps': '8-12',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Leg Press',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Lunges',
                'sets': 3,
                'reps': '10-12 per leg',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Leg Extensions',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Leg Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Calf Raises',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            }
        ]
    },
    {
        'id': 4,
        'title': 'Day 4: Shoulders and Abs',
        'exercises': [
            {
                'name': 'Dumbbell Shoulder Press',
                'sets': 3,
                'reps': '8-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Lateral Raises',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Rear Delt Flyes',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Hanging Leg Raises',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Planks',
                'sets': 3,
                'reps': '30-60 seconds',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Russian Twists',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            }
        ]
    },
    {
        'id': 5,
        'title': 'Day 5: Chest and Triceps',
        'exercises': [
            {
                'name': 'Incline Bench Press',
                'sets': 4,
                'reps': '8-12',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Dumbbell Chest Press',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Cable Crossovers',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Tricep Dips',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Overhead Rope Extensions',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Tricep Kickbacks',
                'sets': 3,
                'reps': '8-10',
                'duration': 40,
                'image_placeholder': True
            }
        ]
    },
    {
        'id': 6,
        'title': 'Day 6: Back and Biceps',
        'exercises': [
            {
                'name': 'Deadlifts',
                'sets': 4,
                'reps': '8-12',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Bent-Over Barbell Rows',
                'sets': 3,
                'reps': '8-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Pull-ups',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Dumbbell Bicep Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Hammer Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            },
            {
                'name': 'Concentration Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 40,
                'image_placeholder': True
            }
        ]
    },
    {
        'id': 7,
        'title': 'Day 7: Legs',
        'exercises': [
            {
                'name': 'Leg Press',
                'sets': 4,
                'reps': '8-12',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Squats',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Lunges',
                'sets': 3,
                'reps': '10-12 per leg',
                'duration': 60,
                'image_placeholder': True
            },
            {
                'name': 'Leg Extensions',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Leg Curls',
                'sets': 3,
                'reps': '10-12',
                'duration': 45,
                'image_placeholder': True
            },
            {
                'name': 'Calf Raises',
                'sets': 3,
                'reps': '12-15',
                'duration': 45,
                'image_placeholder': True
            }
        ]
    }
]

def get_exercise_image(exercise_name):
    """Get the image filename for a given exercise"""
    # Look for exact matches first
    if exercise_name in EXERCISE_IMAGES:
        return EXERCISE_IMAGES[exercise_name]
    
    # Look for partial matches
    for key, value in EXERCISE_IMAGES.items():
        if key.lower() in exercise_name.lower() or exercise_name.lower() in key.lower():
            return value
    
    return None

@ensure_csrf_cookie
def routine_list(request):
    """View function for the home page displaying all fitness routines"""
    # Add image paths to exercises
    for routine in fitness_routines:
        for exercise in routine['exercises']:
            image_path = get_exercise_image(exercise['name'])
            if image_path:
                # Use static URL instead of media for content that's in the content directory
                exercise['image_path'] = f'/static/{image_path}'
            else:
                exercise['image_path'] = None

    # Get workout history - limited to last 6
    workout_history = WorkoutHistory.objects.all()[:3]  # Get last 3 workouts

    context = {
        'routines': fitness_routines,
        'page_title': 'Weekly Workout Routine',
        'workout_history': workout_history
    }
    return render(request, 'hello/routine.html', context)

def save_workout(request):
    """Save completed workout data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            workout = WorkoutHistory.objects.create(
                day_id=data['dayId'],
                day_title=data['dayTitle'],
                duration=data['duration'],
                completed_exercises=data['completedExercises']
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Workout saved successfully',
                'id': workout.id
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
