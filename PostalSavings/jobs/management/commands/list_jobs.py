# myapp/management/commands/list_jobs.py
from django.core.management.base import BaseCommand, CommandError
from jobs.models import Job


class Command(BaseCommand):
    help = "List jobs from the database with sorting and limit options"

    def add_arguments(self, parser):
        # 可选命名参数：限制显示的记数
        """

        位置参数是必须按顺序在命令行中提供的参数，参数名没有前缀（如 -- 或 -）。
        在 parser.add_argument 中，参数名不以 - 或 -- 开头。

        """
        parser.add_argument(
            # 'limit',  # 改为位置参数
            '--limit',  # 改为命名参数
            type=int,
            default=10,
            help='Number of jobs to display (default: 10)',
        )
        parser.add_argument(
            '--sort',
            choices=['asc', 'desc'],
            default='desc',
            help='Sort by created_at: asc (oldest first) or desc (newest first)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display detailed information including description',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        sort = options['sort']
        verbose = options['verbose']

        # 确保 limit 是正数
        if limit <= 0:
            raise CommandError("Limit must be a positive integer")

        # 根据 sort 参数设置排序
        order_field = 'created_at' if sort == 'asc' else '-created_at'

        try:
            # 查询 Job 对象
            # print(limit)
            jobs = Job.objects.order_by(order_field)[:limit]
            if not jobs:
                self.stdout.write("No jobs found in the database", self.style.WARNING)
                return

            # 输出结果
            self.stdout.write(f"Listing {len(jobs)} jobs (sorted by created_at: {sort}):")
            for job in jobs:
                if verbose:
                    output = f"{job.title} - {job.created_at} - {job.description}"
                else:
                    output = f"{job.title} - {job.created_at}"
                self.stdout.write(output)
            self.stdout.write(f"Total: {len(jobs)} jobs displayed", self.style.SUCCESS)

        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")

