import tensorflow as tf
from dialogue import Dialogue
from models import Seq2Seq

def train(model, hparams):

    with tf.Session() as sess:
        checkpoint = tf.train.get_checkpoint_state('./model')
        if checkpoint and checkpoint.model_checkpoint_path:
            model.saver.restore(sess, checkpoint.model_checkpoint_path)
        else:
            sess.run(tf.global_variables_initializer())
        for epoch in range(901, hparams.total_epochs):
            epoch_loss = 0
            for batch in range(hparams.total_batch):
                enc_batch, dec_batch, target_batch, enc_seq_len, dec_seq_len, max_len = dialogue.next_batch(hparams.batch_size)
                _cost, _ = sess.run([model.loss, model.train_op], feed_dict={model.source: enc_batch,
                                                                             model.target_input: dec_batch,
                                                                             model.target_output: target_batch,
                                                                             model.source_seq_length: enc_seq_len,
                                                                             model.target_seq_length: dec_seq_len})

                epoch_loss += _cost / hparams.total_batch
            if epoch % 100 == 0:
                print(epoch, epoch_loss)
                model.saver.save(sess, './model/seq2seq', global_step=epoch)


dialogue = Dialogue()

hparams = tf.contrib.training.HParams(total_epochs=5000,
                                      num_units=128,
                                      learning_rate=0.001,
                                      voc_size=dialogue.voc_size,
                                      embedding_size=100,
                                      batch_size=100,
                                      total_batch=len(dialogue.seq_data) // 100)

train_model = Seq2Seq(hparams, 'train')
print("start")
train(train_model, hparams)

