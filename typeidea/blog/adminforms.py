from django import forms


class PostAdminForm(forms.ModelForm):
    # 我们希望文章描述字段能够以 textarea 也就是多行多列的方式展示
    description = forms.CharField(label="摘要",
                                  widget=forms.Textarea,
                                  required=False)  # (N)!: 这个 required 是 html 知识

