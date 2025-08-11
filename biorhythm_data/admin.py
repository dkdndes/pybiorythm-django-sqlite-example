from django.contrib import admin
from django.utils.html import format_html
from .models import Person, BiorhythmCalculation, BiorhythmData, BiorhythmAnalysis


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthdate', 'age_in_days', 'get_biorhythm_data_count', 'created_at']
    list_filter = ['created_at', 'birthdate']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'age_in_days']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'birthdate', 'email')
        }),
        ('Additional Info', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'age_in_days'),
            'classes': ('collapse',)
        }),
    )

    def get_biorhythm_data_count(self, obj):
        count = obj.get_biorhythm_data_count()
        return format_html('<strong>{}</strong> data points', count)
    get_biorhythm_data_count.short_description = 'Data Points'


@admin.register(BiorhythmCalculation)
class BiorhythmCalculationAdmin(admin.ModelAdmin):
    list_display = ['person', 'date_range_str', 'days_calculated', 'calculation_date', 'pybiorythm_version']
    list_filter = ['calculation_date', 'pybiorythm_version']
    search_fields = ['person__name', 'notes']
    readonly_fields = ['calculation_date']
    date_hierarchy = 'calculation_date'
    
    fieldsets = (
        ('Calculation Info', {
            'fields': ('person', 'start_date', 'end_date', 'days_calculated', 'target_date')
        }),
        ('Metadata', {
            'fields': ('calculation_date', 'pybiorythm_version', 'notes'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BiorhythmData)
class BiorhythmDataAdmin(admin.ModelAdmin):
    list_display = ['person', 'date', 'days_alive', 'physical_display', 'emotional_display', 
                   'intellectual_display', 'critical_cycles_display']
    list_filter = ['date', 'is_physical_critical', 'is_emotional_critical', 'is_intellectual_critical', 'person']
    search_fields = ['person__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'cycle_summary', 'critical_cycles']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('person', 'calculation', 'date', 'days_alive')
        }),
        ('Biorhythm Values', {
            'fields': ('physical', 'emotional', 'intellectual')
        }),
        ('Critical Days', {
            'fields': ('is_physical_critical', 'is_emotional_critical', 'is_intellectual_critical', 'critical_cycles'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'cycle_summary'),
            'classes': ('collapse',)
        }),
    )

    def physical_display(self, obj):
        color = self._get_cycle_color(obj.physical)
        return format_html('<span style="color: {}; font-weight: bold;">{:.3f}</span>', color, obj.physical)
    physical_display.short_description = 'Physical'

    def emotional_display(self, obj):
        color = self._get_cycle_color(obj.emotional)
        return format_html('<span style="color: {}; font-weight: bold;">{:.3f}</span>', color, obj.emotional)
    emotional_display.short_description = 'Emotional'

    def intellectual_display(self, obj):
        color = self._get_cycle_color(obj.intellectual)
        return format_html('<span style="color: {}; font-weight: bold;">{:.3f}</span>', color, obj.intellectual)
    intellectual_display.short_description = 'Intellectual'

    def critical_cycles_display(self, obj):
        critical = obj.critical_cycles
        if critical:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', ', '.join(critical))
        return format_html('<span style="color: green;">None</span>')
    critical_cycles_display.short_description = 'Critical Cycles'

    def _get_cycle_color(self, value):
        """Get color based on cycle value."""
        if value > 0.5:
            return '#006400'  # Dark green for high positive
        elif value > 0:
            return '#32CD32'  # Light green for positive
        elif value > -0.5:
            return '#FF6347'  # Tomato for negative
        else:
            return '#8B0000'  # Dark red for low negative


@admin.register(BiorhythmAnalysis)
class BiorhythmAnalysisAdmin(admin.ModelAdmin):
    list_display = ['person', 'analysis_type', 'date_range_str', 'data_points_analyzed', 'analysis_date']
    list_filter = ['analysis_type', 'analysis_date']
    search_fields = ['person__name', 'summary']
    readonly_fields = ['analysis_date']
    date_hierarchy = 'analysis_date'
    
    fieldsets = (
        ('Analysis Info', {
            'fields': ('person', 'analysis_type', 'start_date', 'end_date', 'data_points_analyzed')
        }),
        ('Results', {
            'fields': ('summary', 'results')
        }),
        ('Metadata', {
            'fields': ('analysis_date', 'analysis_parameters'),
            'classes': ('collapse',)
        }),
    )

    def date_range_str(self, obj):
        return f"{obj.start_date} to {obj.end_date}"
    date_range_str.short_description = 'Date Range'
