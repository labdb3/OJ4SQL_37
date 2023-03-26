from django.urls import path

from . import views

urlpatterns = [
    path('<int:gid>/<int:pno>', views.problem_list, name='problem_list'),
    path('content/description/<int:pid>/', views.problem_content_description,
         name='problem_content_description'),
    path('content/description/<int:pid>/interpret_solution', views.problem_content_interpret_solution,
         name='problem_content_interpret_solution'),
    path('content/submission/<int:pid>/<int:pno>',
         views.problem_content_submission, name='problem_content_submission'),
    path('content/submission/code_detail/<int:sid>',
         views.problem_content_submission_details, name='problem_content_submission_details'),
    path('content/solution/<int:pno>', views.problem_content_solution,
         name='problem_content_solution'),
    path('content/submit/<int:pid>', views.problem_code_submit,
         name='problem_code_submit'),
]
