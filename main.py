import frontmatter
import calendar

def define_env(env):
    
    @env.macro
    def grid_entry(path):
        page = frontmatter.load(path)
        
        name = page['name']
        start_month = calendar.month_abbr[int(page['start_month'])]
        start_year = page['start_year']
        end_month = calendar.month_abbr[int(page['end_month'])]
        end_year = page['end_year']


        md = '\n'.join([
            f"- **{name}**",
            "\t",
            f"\t> {start_month} {start_year} - {end_month} {end_year}"
        ])
        
        if page is None:
            return "noooo"
        else:
            return md
