"""Redoing migrations

Revision ID: dca5a3c19137
Revises: 
Create Date: 2023-04-17 10:10:49.608618

"""
import flask_security
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dca5a3c19137'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Configuration',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('session_sz', sa.Integer(), nullable=True),
    sa.Column('live_transcribe', sa.Boolean(), nullable=True),
    sa.Column('visualize_mic', sa.Boolean(), nullable=True),
    sa.Column('auto_trim', sa.Boolean(), nullable=True),
    sa.Column('analyze_sound', sa.Boolean(), nullable=True),
    sa.Column('auto_gain_control', sa.Boolean(), nullable=True),
    sa.Column('noise_suppression', sa.Boolean(), nullable=True),
    sa.Column('channel_count', sa.Integer(), nullable=True),
    sa.Column('sample_rate', sa.Integer(), nullable=True),
    sa.Column('sample_size', sa.Integer(), nullable=True),
    sa.Column('blob_slice', sa.Integer(), nullable=True),
    sa.Column('audio_codec', sa.String(), nullable=True),
    sa.Column('video_w', sa.Integer(), nullable=True),
    sa.Column('video_h', sa.Integer(), nullable=True),
    sa.Column('video_codec', sa.String(), nullable=True),
    sa.Column('has_video', sa.Boolean(), nullable=True),
    sa.Column('trim_threshold', sa.Float(), nullable=True),
    sa.Column('too_low_threshold', sa.Float(), nullable=True),
    sa.Column('too_high_threshold', sa.Float(), nullable=True),
    sa.Column('too_high_frames', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('permissions', flask_security.datastore.AsaList(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('fs_uniquifier', sa.String(length=64), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=64), nullable=True),
    sa.Column('current_login_ip', sa.String(length=64), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('tf_primary_method', sa.String(length=64), nullable=True),
    sa.Column('tf_totp_secret', sa.String(length=255), nullable=True),
    sa.Column('tf_phone_number', sa.String(length=128), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('us_totp_secrets', sa.Text(), nullable=True),
    sa.Column('fs_webauthn_user_handle', sa.String(length=64), nullable=True),
    sa.Column('mf_recovery_codes', flask_security.datastore.AsaList(), nullable=True),
    sa.Column('us_phone_number', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('sex', sa.String(length=255), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('dialect', sa.String(length=255), nullable=True),
    sa.Column('audio_setup', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier'),
    sa.UniqueConstraint('fs_webauthn_user_handle'),
    sa.UniqueConstraint('us_phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Collection',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('assigned_user_id', sa.Integer(), nullable=True),
    sa.Column('is_multi_speaker', sa.Boolean(), nullable=True),
    sa.Column('configuration_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('sort_by', sa.String(), nullable=True),
    sa.Column('num_tokens', sa.Integer(), nullable=True),
    sa.Column('num_recorded_tokens', sa.Integer(), nullable=True),
    sa.Column('num_invalid_tokens', sa.Integer(), nullable=True),
    sa.Column('has_zip', sa.Boolean(), nullable=True),
    sa.Column('zip_token_count', sa.Integer(), nullable=True),
    sa.Column('zip_created_at', sa.DateTime(), nullable=True),
    sa.Column('is_dev', sa.Boolean(), nullable=True),
    sa.Column('verify', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['assigned_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['configuration_id'], ['Configuration.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('Mos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('form_text', sa.String(), nullable=True),
    sa.Column('help_text', sa.String(), nullable=True),
    sa.Column('done_text', sa.String(), nullable=True),
    sa.Column('use_latin_square', sa.Boolean(), nullable=True),
    sa.Column('show_text_in_test', sa.Boolean(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('num_samples', sa.Integer(), nullable=True),
    sa.Column('num_participants', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['Collection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PrioritySession',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('has_video', sa.Boolean(), nullable=True),
    sa.Column('is_secondarily_verified', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('verified_by', sa.Integer(), nullable=True),
    sa.Column('secondarily_verified_by', sa.Integer(), nullable=True),
    sa.Column('is_dev', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['Collection.id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['secondarily_verified_by'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['verified_by'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Session',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('has_video', sa.Boolean(), nullable=True),
    sa.Column('is_secondarily_verified', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('has_priority', sa.Boolean(), nullable=True),
    sa.Column('verified_by', sa.Integer(), nullable=True),
    sa.Column('secondarily_verified_by', sa.Integer(), nullable=True),
    sa.Column('is_dev', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['Collection.id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['secondarily_verified_by'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['verified_by'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('original_fname', sa.String(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('marked_as_bad', sa.Boolean(), nullable=True),
    sa.Column('num_recordings', sa.Integer(), nullable=True),
    sa.Column('pron', sa.String(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['Collection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MosInstance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mos_id', sa.Integer(), nullable=True),
    sa.Column('is_synth', sa.Boolean(), nullable=True),
    sa.Column('voice_idx', sa.Integer(), nullable=True),
    sa.Column('utterance_idx', sa.Integer(), nullable=True),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('selected', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['mos_id'], ['Mos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Recording',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('original_fname', sa.String(), nullable=True),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('priority_session_id', sa.Integer(), nullable=True),
    sa.Column('sr', sa.Integer(), nullable=True),
    sa.Column('num_channels', sa.Integer(), nullable=True),
    sa.Column('latency', sa.Float(), nullable=True),
    sa.Column('auto_gain_control', sa.Boolean(), nullable=True),
    sa.Column('echo_cancellation', sa.Boolean(), nullable=True),
    sa.Column('noise_suppression', sa.Boolean(), nullable=True),
    sa.Column('analysis', sa.String(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('bit_depth', sa.Integer(), nullable=True),
    sa.Column('transcription', sa.String(), nullable=True),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('file_id', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('wav_path', sa.String(), nullable=True),
    sa.Column('start', sa.Float(), nullable=True),
    sa.Column('end', sa.Float(), nullable=True),
    sa.Column('marked_as_bad', sa.Boolean(), nullable=True),
    sa.Column('has_video', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('is_secondarily_verified', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['priority_session_id'], ['PrioritySession.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['Session.id'], ),
    sa.ForeignKeyConstraint(['token_id'], ['Token.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CustomRecording',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('original_fname', sa.String(), nullable=True),
    sa.Column('mos_instance_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('copied_recording', sa.Boolean(), nullable=True),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('file_id', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('wav_path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['mos_instance_id'], ['MosInstance.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CustomToken',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('mos_instance_id', sa.Integer(), nullable=True),
    sa.Column('original_fname', sa.String(), nullable=True),
    sa.Column('copied_token', sa.Boolean(), nullable=True),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('marked_as_bad', sa.Boolean(), nullable=True),
    sa.Column('pron', sa.String(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['mos_instance_id'], ['MosInstance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MosRating',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('mos_instance_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('placement', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mos_instance_id'], ['MosInstance.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mos_instance_id', 'user_id')
    )
    op.create_table('Rating',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('recording_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['Recording.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Verification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('verified_by', sa.Integer(), nullable=True),
    sa.Column('recording_id', sa.Integer(), nullable=True),
    sa.Column('volume_is_low', sa.Boolean(), nullable=True),
    sa.Column('volume_is_high', sa.Boolean(), nullable=True),
    sa.Column('recording_has_glitch', sa.Boolean(), nullable=True),
    sa.Column('recording_has_wrong_wording', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('is_secondary', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['recording_id'], ['Recording.id'], ),
    sa.ForeignKeyConstraint(['verified_by'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Trim',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('start', sa.Float(), nullable=True),
    sa.Column('end', sa.Float(), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('verification_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['verification_id'], ['Verification.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Trim')
    op.drop_table('Verification')
    op.drop_table('Rating')
    op.drop_table('MosRating')
    op.drop_table('CustomToken')
    op.drop_table('CustomRecording')
    op.drop_table('Recording')
    op.drop_table('MosInstance')
    op.drop_table('Token')
    op.drop_table('Session')
    op.drop_table('PrioritySession')
    op.drop_table('Mos')
    op.drop_table('roles_users')
    op.drop_table('Collection')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('Configuration')
    # ### end Alembic commands ###
