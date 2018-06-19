from music_project import models


def __get_user_relating_data__(user, model):
    """
    :param user current oauthentication user:
    :param model current model for filter current:
    :return: filtered queryset
    """
    data_id = __get_songs_related_id__(user, model.__name__)
    return model.objects.filter(id__in=data_id)

def __get_songs_related_id__(current_user, model_name):
    return current_user.song_set.all().values_list(model_name.lower(), flat=True)

def get_playlist(id):
    return models.Playlist.objects.get(pk=id)