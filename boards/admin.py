from email.headerregistry import Group
from django.contrib import admin
from boards.models import Board, Post, Topic
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin



# customize the Board model 
class InlineTopic(admin.StackedInline):
    model = Topic  
    extra = 2  # show 2 samples

class BoardAdmin(admin.ModelAdmin):
    # inlines should have Foriegn key with the other model
    inlines = [InlineTopic]  


# customize the Topic model 
class TopicAdmin(admin.ModelAdmin):
    fields = ('subject', 'created_by',)
    list_display = ('subject', 'board', 'created_by', 'combine_subject_and_board',)
    list_display_links = ('board',)
    list_editable = ('subject',)  # the editable fields might not be in the links list
    list_filter = ('created_by', 'board')
    search_fields = ('board', 'created_by')

    def combine_subject_and_board(self, obj):
        return " {}__{} " . format(obj.subject , obj.board)


# Import / Export database (csv, excel...)
@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    pass

# admin.site.register(Topic, TopicAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Post)
admin.site.unregister(Group)

# Customize header and title
admin.site.site_header = "Boards"
admin.site.site_title = "Boards Admin Panel"
